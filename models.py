from sqlalchemy.orm import Mapped
from sqlalchemy import Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, mapped_column


engine = create_engine("sqlite:///my_films.db")
Base = declarative_base()


class ProductType(Base):
    __tablename__ = "product_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    product_type_id: Mapped[int] = mapped_column(Integer)
