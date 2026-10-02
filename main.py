from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product as PydanticProduct
from database import SessionLocal, engine
import database_models

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def greet():
    return "Welcome to FASTAPI"

@app.get('/products')
def get_all_products(db: Session = Depends(get_db)):
    # .query().all() is the SQLAlchemy version of "SELECT * FROM product;"
    products = db.query(database_models.Product).all()
    return products

@app.post('/product')
def add_product(product: PydanticProduct, db: Session = Depends(get_db)):
    new_db_product = database_models.Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    db.add(new_db_product)
    db.commit()
    db.refresh(new_db_product)
    return new_db_product


@app.put('/product/{id}')
def update_product(id: int, product: PydanticProduct, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    
    db.commit()
    db.refresh(db_product)
    
    return {
        "status": "Updated",
        "message": db_product
    }


@app.delete('/product/{id}')
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db.delete(db_product)
    db.commit()
    
    return {
        "message": "Product deleted successfully", 
        "deleted_product": {"id": id, "name": db_product.name}
    }