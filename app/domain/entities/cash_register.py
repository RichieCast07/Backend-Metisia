from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import CashRegisterStatus

@dataclass
class CashRegister:
    id: str
    business_id: str
    status: CashRegisterStatus
    opening_amount: float
    closing_amount: Optional[float]
    opened_at: datetime
    closed_at: Optional[datetime]
    opened_by: str
