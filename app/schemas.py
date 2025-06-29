from fastapi_pagination import Params
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Annotated

class ManufacturerEnum(str, Enum):
  SIMAGIC = 'SIMAGIC'
  MOZA = 'MOZA'

class CategoryEnum(str, Enum):
  WHEEL_BASE = 'Wheel base'
  PEDALS = 'Pedals'
  WHEELS = 'Wheels'


class Product(BaseModel):
  name: Annotated[str, Field(min_length=3, max_length=30)]
  category: CategoryEnum
  manufacturer: ManufacturerEnum
  price: Annotated[float, Field(gt=0)]
  quantity: Annotated[int, Field(gt=0)]

class ProductPatch(BaseModel):
  name: Annotated[str, Field(min_length=3, max_length=30)] | None = None
  category: CategoryEnum | None = None
  manufacturer: ManufacturerEnum | None = None
  price: Annotated[float, Field(gt=0)] | None = None

class ProductsSearchQueries(Params):
  size: int = 20