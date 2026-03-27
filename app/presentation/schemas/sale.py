from pydantic import BaseModel
from typing import Optional, List
from app.domain.entities.enums import PaymentMethod
from datetime import datetime

class SaleItemCreate(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

class WorkerParticipationCreate(BaseModel):
    worker_id: str
    percentage: float

class SaleCreate(BaseModel):
    worker_id: Optional[str]
    promotion_id: Optional[str]
    cash_register_id: str
    subtotal: float
    discount: float
    total: float
    payment_method: PaymentMethod
    notes: Optional[str]
    items: List[SaleItemCreate]
    participations: Optional[List[WorkerParticipationCreate]] = []

class SaleResponse(BaseModel):
    id: str
    business_id: str
    worker_id: Optional[str]
    promotion_id: Optional[str]
    cash_register_id: str
    subtotal: float
    discount: float
    total: float
    payment_method: PaymentMethod
    notes: Optional[str]
    created_at: datetime
    items: List[SaleItemCreate]
    participations: Optional[List[WorkerParticipationCreate]]

    class Config:
        orm_mode = True
