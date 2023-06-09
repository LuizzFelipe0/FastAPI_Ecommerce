from sqlalchemy.orm import Session
import core.schemas as schemas
import data.models as models


class ProductController:
    async def create(db: Session, product: schemas.ProductCreate):
        db_product = models.Product(name=product.name, price=product.price, description=product.description, category_id=product.category_id)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    def get_by_id(db: Session, _id):
        return db.query(models.Product).filter(models.Product.id == _id).first()
 
    def get_by_name(db: Session, name):
        return db.query(models.Product).filter(models.Product.name == name).first()
 
    def get_all(db: Session):
        return db.query(models.Product).filter(models.Product.is_deleted == False).all()
 
    async def delete(db: Session, product_id):
        db_product = db.query(models.Product).filter_by(id=product_id).first()
        if db_product:
            db_product.is_deleted = True
            db.commit()
            return db_product
    
    async def update(db: Session, product_data):
        db.merge(product_data)
        db.commit()
        return product_data

    
class CategoryController:
    async def create(db: Session, category: schemas.CategoryCreate):
        db_category = models.Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
        
    def get_by_id(db: Session, _id: int):
        return db.query(models.Category).filter(models.Category.id == _id).first()
    
    def get_by_name(db: Session, name: str):
        return db.query(models.Category).filter(models.Category.name == name).first()
    
    def get_all(db: Session):
        return db.query(models.Category).filter(models.Category.is_deleted == False).all()
    
    async def delete(db: Session, _id: int):
        db_category = db.query(models.Category).filter_by(id=_id).first()
        if db_category:
            db_category.is_deleted = True
            db.commit()
            return db_category
        
    async def update(db: Session, category_data):
        db.merge(category_data)
        db.commit()
        return category_data
