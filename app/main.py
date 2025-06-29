from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
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
def get_products(
  params: schemas.ProductsSearchQueries = Depends(), 
  manufacturer: Optional[str] = Query(None),
  sort_by: Optional[str] = Query(None), 
  sort_order: Optional[str] = Query("asc"),
  db: Session = Depends(get_db)
  ):

  if params.model_dump()["size"] not in [20, 30, 40]:
    raise HTTPException(status_code=422, detail="Size must be one of: 20, 30 or 40")
  
  query = db.query(models.Product)

  if manufacturer:
    query = query.filter(models.Product.manufacturer == manufacturer)

  if sort_by:

    allowed_sort_fields = ["name", "price", "quantity"]
    sort_orders = ["asc", "desc"]

    if sort_by not in allowed_sort_fields:

      raise HTTPException(status_code=422, detail=f"Sort must be one of following: {', '.join(allowed_sort_fields)}")
    
    if sort_order not in sort_orders:
      raise HTTPException(status_code=422, detail="Sort order must be either asc or desc")
  
    sort_column = getattr(models.Product, sort_by)
    if sort_order == "desc":
      sort_column = sort_column.desc()
    else:
      sort_column = sort_column.asc()
    query = db.query(models.Product).order_by(sort_column)

  return paginate(db, query, params)

add_pagination(app)

@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id == product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  return product

@app.post("/products", status_code=201)
def add_product(product: schemas.Product, db: Session = Depends(get_db)):

  found = db.query(models.Product).filter(models.Product.name == product.name).first()

  if found:
    if product.quantity is not None:
      found.quantity = (found.quantity or 0) + product.quantity
      db.commit()
      db.refresh(found)
    return found

  db_product = models.Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)

  return {
    "message": "Product added"
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