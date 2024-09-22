import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import Base, Product, ProductType  # Импортируйте ваши модели и приложение
from app.main import app, get_db

# Создание тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базы данных
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
    # Заполнение тестовой базы данных
    product_type = ProductType(name="Electronics")
    test_db.add(product_type)
    test_db.commit()

    product = Product(name="Smartphone", product_type_id=product_type.id)
    test_db.add(product)
    test_db.commit()


def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Smartphone"
