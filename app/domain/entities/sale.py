from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import PaymentMethod

@dataclass
class Sale:
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
