from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    id: str
    business_id: str
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
    image_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
