from dataclasses import dataclass
from datetime import datetime
from .enums import IngredientMovementType

@dataclass
class IngredientMovement:
    id: str
    business_id: str
    ingredient_id: str
    type: IngredientMovementType
    quantity: float
    reason: str
    date: datetime
