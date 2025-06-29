from pydantic import BaseModel

class ProductCreate(BaseModel):
  name: str
  category: str
  manufacturer: str
  price: float