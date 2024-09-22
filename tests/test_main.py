import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Product, ProductType
from app.main import app, get_db

# Создание тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_db():
    # Создание сессии для тестирования
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
def client(test_db):
    # Создание клиента FastAPI
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module", autouse=True)
def setup_database(test_db):
    # Тестовое заполнение БД
    product_type = ProductType(name="Молочное")
    test_db.add(product_type)
    test_db.commit()

    product = Product(name="Сыр", product_type_id=product_type.id)
    test_db.add(product)
    test_db.commit()


def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Сыр"


def test_create_product(client):
    product_data = {
        "name": "Колбаса",
        "product_type_name": "Мясное"
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    created_product = response.json()
    assert created_product["name"] == product_data["name"]
    assert created_product["product_type"]["name"] == product_data["product_type_name"]


def test_get_product(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "name" in response.json()
    assert response.json()["name"] == "Сыр"


def test_get_products_by_type(client):
    response = client.get("/products/type/2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["product_type"]["name"] == "Мясное"
