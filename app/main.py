# Добавление нового товара (POST /products)
# Получение товара по его ID (GET /products/{id})
# Получение товаров по типу (GET /products/type/{type_id})
import uvicorn
from models import Session, Product, ProductType
from sqlalchemy.orm import joinedload
from fastapi import FastAPI
from schemas import ProductResponse

app = FastAPI()


@app.get("/products", response_model=list[ProductResponse])
async def get_products():
    with Session() as session:
        products = session.query(Product).options(joinedload(Product.product_type)).all()
    return products


@app.get("/products/{product_id}", response_model=list[ProductResponse])
async def get_products(product_id: int):
    with Session() as session:
        product = (session.query(Product)
                   .filter(Product.id == product_id)
                   .options(joinedload(Product.product_type))
                   .all())
    return product


@app.get("/products/type/{type_id}", response_model=list[ProductResponse])
async def get_products(type_id: int):
    with Session() as session:
        product = (session.query(Product)
                   .join(Product.product_type)
                   .filter(ProductType.id == type_id)
                   .options(joinedload(Product.product_type))
                   .all())
    return product


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
