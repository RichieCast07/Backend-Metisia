from app.domain.repositories.sale_repository import ISaleRepository
from app.domain.repositories.expense_repository import IExpenseRepository
from app.domain.entities.sale import Sale
from app.domain.entities.expense import Expense
from typing import List
from datetime import date, datetime
from collections import defaultdict

class DailySalesReport:
    def __init__(self, sale_repo: ISaleRepository, expense_repo: IExpenseRepository):
        self.sale_repo = sale_repo
        self.expense_repo = expense_repo
    async def __call__(self, business_id: str, day: date):
        sales = await self.sale_repo.get_all(business_id)
        expenses = await self.expense_repo.get_all(business_id)
        total_ventas = sum(s.total for s in sales if s.created_at.date() == day)
        total_gastos = sum(e.amount for e in expenses if e.date.date() == day)
        ganancia = total_ventas - total_gastos
        return {"total_ventas": total_ventas, "total_gastos": total_gastos, "ganancia": ganancia}

class SalesByPaymentMethod:
    def __init__(self, sale_repo: ISaleRepository):
        self.sale_repo = sale_repo
    async def __call__(self, business_id: str, start: date, end: date):
        sales = await self.sale_repo.get_all(business_id)
        result = defaultdict(float)
        for s in sales:
            if start <= s.created_at.date() <= end:
                result[s.payment_method] += s.total
        return dict(result)

class TopProducts:
    def __init__(self, sale_repo: ISaleRepository):
        self.sale_repo = sale_repo
    async def __call__(self, business_id: str, start: date, end: date, limit: int = 10):
        sales = await self.sale_repo.get_all(business_id)
        product_counter = defaultdict(float)
        for s in sales:
            if start <= s.created_at.date() <= end:
                for item in getattr(s, "items", []):
                    product_counter[item.product_name] += item.quantity
        return sorted(product_counter.items(), key=lambda x: x[1], reverse=True)[:limit]
