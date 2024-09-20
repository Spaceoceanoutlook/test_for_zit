from pydantic import BaseModel


class ProductTypeResponse(BaseModel):
    id: int
    name: str


class ProductResponse(BaseModel):
    id: int
    name: str
    product_type: ProductTypeResponse

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    product_type_name: str
