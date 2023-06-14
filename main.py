from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import core.schemas as schemas
import data.models as models
from data.database import get_db, engine
from core.controller import CategoryController,ProductController
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

router = FastAPI(title="E-commerce FastAPI",
    description="API with Swagger and Sqlalchemy",)

models.Base.metadata.create_all(bind=engine)

@router.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@router.get('/',tags=["Root"])
def root():
    return {'Message': 'Simple E-commerce API to assist in Future Projects'}



# Routes For Products   

@router.post('/products', tags=["Products"],response_model=schemas.Product,status_code=201)
async def create_item(product_request: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_products = ProductController.get_by_name(db, name=product_request.name)
    if db_products:
        raise HTTPException(status_code=400, detail="Product already exists!")

    return await ProductController.create(db=db, product=product_request)

@router.get('/products', tags=["Products"],response_model=List[schemas.Product])
def get_all_products(name: Optional[str] = None, db: Session = Depends(get_db)):
    if name:
        products =[]
        db_products = ProductController.get_by_name(db, name)
        products.routerend(db_products)
        return products
    else:
        return ProductController.get_all(db)


@router.get('/products/{id}',tags=["Products"],response_model=schemas.Product)
def get_item(id: int,db: Session = Depends(get_db)):
    db_products = ProductController.get_by_id(db,id)
    if db_products is None:
        raise HTTPException(status_code=404, detail="Product not found with the given ID")
    return db_products

@router.delete('/products/{id}', tags=["Products"])
async def delete_item(id: int,db: Session = Depends(get_db)):
    db_products = ProductController.get_by_id(db,id)
    if db_products is None:
        raise HTTPException(status_code=404, detail="Product not found with the given ID")
    await ProductController.delete(db,id)
    return "Product deleted successfully!"


@router.put('/products/{id}', tags=["Products"],response_model=schemas.Product)
async def update_item(id: int,product_request: schemas.Product, db: Session = Depends(get_db)):
    db_products = ProductController.get_by_id(db, id)
    if db_products:
        update_item_encoded = jsonable_encoder(product_request)
        db_products.name = update_item_encoded['name']
        db_products.price = update_item_encoded['price']
        db_products.description = update_item_encoded['description']
        db_products.category_id = update_item_encoded['category_id']
        return await ProductController.update(db=db, product_data=db_products)
    else:
        raise HTTPException(status_code=400, detail="Product not found with the given ID")
    
    
# Routes For Categories   
    
@router.post('/category', tags=["Categories"],response_model=schemas.Category,status_code=201)
async def create_category(category_request: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryController.get_by_name(db, name=category_request.name)
    print(db_category)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists!")

    return await CategoryController.create(db=db, category=category_request)

@router.get('/category', tags=["Categories"],response_model=List[schemas.Category])
def get_all_categories(name: Optional[str] = None,db: Session = Depends(get_db)):
    if name:
        categorys =[]
        db_category = CategoryController.get_by_name(db,name)
        print(db_category)
        categorys.routerend(db_category)
        return categorys
    else:
        return CategoryController.get_all(db)
    
@router.get('/category/{category_id}', tags=["Categories"],response_model=schemas.Category)
def get_category(category_id: int,db: Session = Depends(get_db)):
    db_category = CategoryController.get_by_id(db,category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found with the given ID")
    return db_category

@router.put('/category/{category_id}', tags=["Categories"],response_model=schemas.Category)
async def update_category(category_id: int , category_request: schemas.Category, db: Session = Depends(get_db)):
    
    db_categories = CategoryController.get_by_id(db, category_id)
    if db_categories:
        update_item_encoded = jsonable_encoder(category_request)
        db_categories.name = update_item_encoded['name']
        return await CategoryController.update(db=db, category_data=db_categories)
    else:
        raise HTTPException(status_code=400, detail="Category not found with the given ID")
    


@router.delete('/category/{category_id}', tags=["Categories"])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = CategoryController.get_by_id(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found with the given ID")
    await CategoryController.delete(db,category_id)
    return "Category deleted successfully!"
    

if __name__ == "__main__":
    uvicorn.run("main:router", port=9000, reload=True)