import pytest
from httpx import ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Product, ProductType
from app.main import app, get_db
import httpx

# Создание тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def test_db():
    # Удаление всех таблиц и создание новой базы данных и таблиц
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Создание сессии для тестирования
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
async def client(test_db):
    async def get_test_db():
        return test_db

    app.dependency_overrides[get_db] = get_test_db

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c

    app.dependency_overrides = {}


@pytest.fixture(scope="module", autouse=True)
def setup_database(test_db):
    # Тестовое заполнение БД
    product_type = ProductType(name="Молочное")
    test_db.add(product_type)
    test_db.commit()

    product = Product(name="Сыр", product_type_id=product_type.id)
    test_db.add(product)
    test_db.commit()


@pytest.mark.asyncio
async def test_get_products(client):
    response = await client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Сыр"


@pytest.mark.asyncio
async def test_create_product(client):
    product_data = {"name": "Колбаса", "product_type_name": "Мясное"}
    response = await client.post("/products", json=product_data)
    assert response.status_code == 200
    created_product = response.json()
    assert created_product["name"] == product_data["name"]
    assert created_product["product_type"]["name"] == product_data["product_type_name"]


@pytest.mark.asyncio
async def test_get_product(client):
    response = await client.get("/products/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "name" in response.json()
    assert response.json()["name"] == "Сыр"


@pytest.mark.asyncio
async def test_get_products_by_type(client):
    response = await client.get("/products/type/2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["product_type"]["name"] == "Мясное"
