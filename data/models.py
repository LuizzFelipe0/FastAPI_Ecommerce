from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from data.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return 'Product(name = %s, price = %s, category_id = %s, is_deleted = %s)' % (self.name, self.price, self.category_id, self.is_deleted)

class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)
    products = relationship("Product", primaryjoin="Category.id == Product.category_id", cascade="all, delete-orphan")
    is_deleted = Column(Boolean, default=False)
    
    def __repr__(self):
        return 'Category(name=%s)' % self.name
