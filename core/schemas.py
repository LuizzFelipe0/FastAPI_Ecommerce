from typing import List, Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price : float
    description: Optional[str] = None
    category_id: int


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass



class CategoryBase(BaseModel):
    name: str


class Category(CategoryBase):
    id: int
    products: List[Product] = []

    class Config:
        orm_mode = True
        
class CategoryCreate(CategoryBase):
    pass
