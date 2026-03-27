from dataclasses import dataclass

@dataclass
class SaleItem:
    id: str
    sale_id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
