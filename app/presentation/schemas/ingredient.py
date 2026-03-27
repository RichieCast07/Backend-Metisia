from pydantic import BaseModel
from typing import Optional
from app.domain.entities.enums import Unit
from datetime import datetime

class IngredientCreate(BaseModel):
    name: str
    unit: Unit
    stock: float
    min_stock: float
    unit_cost: float
    supplier: Optional[str]

class IngredientUpdate(BaseModel):
    name: Optional[str]
    unit: Optional[Unit]
    stock: Optional[float]
    min_stock: Optional[float]
    unit_cost: Optional[float]
    supplier: Optional[str]

class IngredientResponse(BaseModel):
    id: str
    business_id: str
    name: str
    unit: Unit
    stock: float
    min_stock: float
    unit_cost: float
    supplier: Optional[str]
    updated_at: datetime

    class Config:
        orm_mode = True
