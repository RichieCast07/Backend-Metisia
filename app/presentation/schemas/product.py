from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
    image_url: Optional[str]
    is_active: Optional[bool] = True

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    image_url: Optional[str]
    is_active: Optional[bool]

class ProductResponse(BaseModel):
    id: str
    business_id: str
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
    image_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
