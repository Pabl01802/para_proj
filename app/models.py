from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  category = Column(String)
  manufacturer = Column(String)
  price = Column(Float)
  quantity = Column(Integer, default=1)