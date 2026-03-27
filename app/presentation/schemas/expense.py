from pydantic import BaseModel
from typing import Optional
from app.domain.entities.enums import ExpenseCategory
from datetime import datetime

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: ExpenseCategory
    date: datetime

class ExpenseUpdate(BaseModel):
    description: Optional[str]
    amount: Optional[float]
    category: Optional[ExpenseCategory]
    date: Optional[datetime]

class ExpenseResponse(BaseModel):
    id: str
    business_id: str
    description: str
    amount: float
    category: ExpenseCategory
    date: datetime
    created_at: datetime

    class Config:
        orm_mode = True
