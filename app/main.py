from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/products", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
  return db.query(models.Product).all()

@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id == product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  return product

@app.post("/products", status_code=201)
def add_product(product: schemas.Product, db: Session = Depends(get_db)):

  db_product = models.Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)

  return {
    "message": "Product created"
  }

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
  with Session(engine) as session:
    product = session.get(models.Product, product_id)
    if not product:
      raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()

  return 