from dataclasses import dataclass

@dataclass
class ProductIngredient:
    id: str
    product_id: str
    ingredient_id: str
    quantity: float
