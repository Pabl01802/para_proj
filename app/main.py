from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal
from . import schemas
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/products", response_model=Page[schemas.Product])
def get_products(params: schemas.ProductsSearchQueries = Depends(), db: Session = Depends(get_db)):
  if  params.model_dump()["size"] not in [20, 30, 40]:
    raise HTTPException(status_code=422, detail="Size must be one of: 20, 30 or 40")

  return paginate(db, db.query(models.Product), params)

add_pagination(app)

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

@app.patch("/products/{product_id}", response_model=schemas.Product)
def modify_product(product_id: int, patch_data: schemas.ProductPatch, db: Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id == product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")

  update_data = patch_data.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(product, key, value)

  db.add(product)
  db.commit()
  db.refresh(product)
  return product