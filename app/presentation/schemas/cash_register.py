from pydantic import BaseModel
from typing import Optional
from app.domain.entities.enums import CashRegisterStatus
from datetime import datetime

class CashRegisterCreate(BaseModel):
    status: CashRegisterStatus
    opening_amount: float
    opened_at: datetime
    opened_by: str

class CashRegisterUpdate(BaseModel):
    status: Optional[CashRegisterStatus]
    closing_amount: Optional[float]
    closed_at: Optional[datetime]
    opened_by: Optional[str]

class CashRegisterResponse(BaseModel):
    id: str
    business_id: str
    status: CashRegisterStatus
    opening_amount: float
    closing_amount: Optional[float]
    opened_at: datetime
    closed_at: Optional[datetime]
    opened_by: str

    class Config:
        orm_mode = True
