from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import Unit

@dataclass
class Ingredient:
    id: str
    business_id: str
    name: str
    unit: Unit
    stock: float
    min_stock: float
    unit_cost: float
    supplier: Optional[str]
    updated_at: datetime
