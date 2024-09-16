import uvicorn
from models import DATABASE_URL, Product, ProductType
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy import create_engine
from fastapi import FastAPI, Depends
from schemas import ProductResponse, ProductCreate

app = FastAPI()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Создание сессии
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", response_model=list[ProductResponse])
async def get_products(session: Session = Depends(get_db)):
    products = session.query(Product).options(joinedload(Product.product_type)).all()
    return products


@app.post("/add_product", response_model=ProductResponse)
async def create_product(product: ProductCreate, session: Session = Depends(get_db)):
    new_product = Product(name=product.name, product_type_id=product.product_type_id)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    print(new_product.product_type)
    return new_product


@app.get("/products/{product_id}", response_model=list[ProductResponse])
async def get_products(product_id: int, session: Session = Depends(get_db)):
    product = (
        session.query(Product)
        .filter(Product.id == product_id)
        .options(joinedload(Product.product_type))
        .all()
    )
    return product


@app.get("/products/type/{type_id}", response_model=list[ProductResponse])
async def get_products(type_id: int, session: Session = Depends(get_db)):
    product = (
        session.query(Product)
        .join(Product.product_type)
        .filter(ProductType.id == type_id)
        .options(joinedload(Product.product_type))
        .all()
    )
    return product


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
