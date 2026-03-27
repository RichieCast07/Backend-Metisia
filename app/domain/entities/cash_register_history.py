from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CashRegisterHistory:
    id: str
    cash_register_id: str
    business_id: str
    opening_amount: float
    closing_amount: Optional[float]
    total_sales: float
    total_expenses: float
    difference: float
    opened_at: datetime
    closed_at: datetime
