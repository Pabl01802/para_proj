from fastapi import FastAPI, Depends
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

@app.get("/products")
def read_products(db: Session = Depends(get_db)):
  return db.query(models.Product).all()

@app.post("/products", status_code=201)
def add_products(product: schemas.ProductCreate, db: Session = Depends(get_db)):

  db_product = models.Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)

  return {
    "message": "created"
  }