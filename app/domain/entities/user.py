from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import BusinessType, Plan

@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    business_name: str
    business_type: BusinessType
    plan: Plan
    created_at: datetime
    last_login_at: Optional[datetime] = None
