from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated

class ManufacturerEnum(str, Enum):
  SIMAGIC = 'SIMAGIC'
  MOZA = 'MOZA'

class CategoryEnum(str, Enum):
  WHEEL_BASE = 'Wheel base'
  PEDALS = 'Pedals'
  WHEELS = 'Wheels'


class ProductCreate(BaseModel):
  name: Annotated[str, Field(min_length=3, max_length=30)]
  category: CategoryEnum
  manufacturer: ManufacturerEnum
  price: Annotated[float, Field(gt=0)]