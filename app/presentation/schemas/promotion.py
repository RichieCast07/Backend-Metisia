from pydantic import BaseModel
from typing import Optional
from app.domain.entities.enums import PromotionType, PromotionApplicableTo
from datetime import datetime

class PromotionCreate(BaseModel):
    name: str
    type: PromotionType
    value: float
    applicable_to: PromotionApplicableTo
    target_id: Optional[str]
    is_active: Optional[bool] = True
    starts_at: datetime
    ends_at: datetime

class PromotionUpdate(BaseModel):
    name: Optional[str]
    type: Optional[PromotionType]
    value: Optional[float]
    applicable_to: Optional[PromotionApplicableTo]
    target_id: Optional[str]
    is_active: Optional[bool]
    starts_at: Optional[datetime]
    ends_at: Optional[datetime]

class PromotionResponse(BaseModel):
    id: str
    business_id: str
    name: str
    type: PromotionType
    value: float
    applicable_to: PromotionApplicableTo
    target_id: Optional[str]
    is_active: bool
    starts_at: datetime
    ends_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
