from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import WorkerPaymentType

@dataclass
class WorkerPayment:
    id: str
    business_id: str
    worker_id: str
    amount: float
    type: WorkerPaymentType
    period: str
    notes: Optional[str]
    paid_at: datetime
