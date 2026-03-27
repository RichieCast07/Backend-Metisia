from dataclasses import dataclass
from datetime import datetime
from .enums import ExpenseCategory

@dataclass
class Expense:
    id: str
    business_id: str
    description: str
    amount: float
    category: ExpenseCategory
    date: datetime
    created_at: datetime
