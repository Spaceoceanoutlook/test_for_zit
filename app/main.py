import uvicorn
from models import Session, Product, ProductType
from sqlalchemy.orm import joinedload
from fastapi import FastAPI
from schemas import ProductResponse, ProductCreate

app = FastAPI()


@app.get("/products", response_model=list[ProductResponse])
async def get_products():
    with Session() as session:
        products = session.query(Product).options(joinedload(Product.product_type)).all()
    return products


@app.post("/add_product", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    with Session() as session:
        new_product = Product(name=product.name, product_type_id=product.product_type_id)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        print(new_product.product_type)
    return new_product


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
