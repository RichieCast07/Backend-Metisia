from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import PromotionType, PromotionApplicableTo

@dataclass
class Promotion:
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
