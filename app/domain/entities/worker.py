from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Worker:
    id: str
    business_id: str
    name: str
    role: str
    phone: Optional[str]
    daily_rate: float
    is_active: bool
    hired_at: datetime
