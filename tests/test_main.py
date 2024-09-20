import pytest
from httpx import AsyncClient
from app.main import app, get_db  # Убедитесь, что путь правильный
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Импортируйте вашу базу моделей

# Создайте тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Используйте SQLite для тестирования
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создайте фикстуру для тестовой базы данных
@pytest.fixture(scope="module")
def test_app():
    # Создайте таблицы
    Base.metadata.create_all(bind=engine)

    yield app  # Возвращаем приложение для тестирования

    # Удалите таблицы после тестов
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Создайте сессию для каждого теста
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
async def client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client  # Здесь мы возвращаем клиент

@pytest.mark.asyncio
async def test_get_products(client, db_session):
    response = await client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_type(client, db_session):
    response = await client.post("/add_type", json={"name": "New Type"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Type"

@pytest.mark.asyncio
async def test_create_product(client, db_session):
    # Сначала создайте тип продукта
    type_response = await client.post("/add_type", json={"name": "Test Type"})
    type_id = type_response.json()["id"]

    response = await client.post("/add_product", json={"name": "New Product", "product_type_id": type_id})
    assert response.status_code == 200
    assert response.json()["name"] == "New Product"

@pytest.mark.asyncio
async def test_get_product_by_id(client, db_session):
    # Сначала создайте продукт
    type_response = await client.post("/add_type", json={"name": "Test Type"})
    type_id = type_response.json()["id"]
    product_response = await client.post("/add_product", json={"name": "New Product", "product_type_id": type_id})
    product_id = product_response.json()["id"]

    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id

@pytest.mark.asyncio
async def test_get_products_by_type(client, db_session):
    # Сначала создайте тип и продукт
    type_response = await client.post("/add_type", json={"name": "Test Type"})
    type_id = type_response.json()["id"]
    await client.post("/add_product", json={"name": "Product 1", "product_type_id": type_id})
    await client.post("/add_product", json={"name": "Product 2", "product_type_id": type_id})

    response = await client.get(f"/products/type/{type_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Должно вернуть 2 продукта
