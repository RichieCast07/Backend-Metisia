from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkerCreate(BaseModel):
    name: str
    role: str
    phone: Optional[str]
    daily_rate: float
    is_active: Optional[bool] = True
    hired_at: datetime

class WorkerUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str]
    phone: Optional[str]
    daily_rate: Optional[float]
    is_active: Optional[bool]
    hired_at: Optional[datetime]

class WorkerResponse(BaseModel):
    id: str
    business_id: str
    name: str
    role: str
    phone: Optional[str]
    daily_rate: float
    is_active: bool
    hired_at: datetime

    class Config:
        orm_mode = True
