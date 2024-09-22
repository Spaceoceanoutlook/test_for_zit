from pydantic import BaseModel, ConfigDict


class ProductTypeResponse(BaseModel):
    id: int
    name: str


class ProductResponse(BaseModel):
    id: int
    name: str
    product_type: ProductTypeResponse

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    product_type_name: str
