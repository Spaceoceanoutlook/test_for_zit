import psycopg2
from psycopg2 import sql
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")


def create_database_if_not_exists(db_name, user, password, host, port):
    """
    Подключение к Postgresql и создание базы данных
    """
    if os.getenv("TESTING"):
        return
    with psycopg2.connect(
        user=user, password=password, dbname=db_name, host=host, port=port
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"),
                [db_name],
            )
            exists = cursor.fetchone()
    if not exists:
        conn = psycopg2.connect(
            user=user, password=password, dbname=db_name, host=host, port=port
        )
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )


create_database_if_not_exists(DB_NAME, USER, PASSWORD, HOST, PORT)
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


Base = declarative_base()


class ProductType(Base):
    __tablename__ = "product_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="product_type"
    )


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_type.id"))

    product_type: Mapped[ProductType] = relationship(
        "ProductType", back_populates="products"
    )
