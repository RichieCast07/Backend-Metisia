from pydantic import BaseModel
from typing import Dict, Any, List, Tuple

class DailySalesReportResponse(BaseModel):
    total_ventas: float
    total_gastos: float
    ganancia: float

class SalesByPaymentMethodResponse(BaseModel):
    data: Dict[str, float]

class TopProductsResponse(BaseModel):
    products: List[Tuple[str, float]]
