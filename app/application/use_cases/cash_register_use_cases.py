from app.domain.repositories.cash_register_repository import ICashRegisterRepository
from app.domain.entities.cash_register import CashRegister
from typing import List
from datetime import datetime

class OpenCashRegister:
    def __init__(self, repo: ICashRegisterRepository):
        self.repo = repo
    async def __call__(self, cash_register: CashRegister) -> CashRegister:
        return await self.repo.create(cash_register)

class CloseCashRegister:
    def __init__(self, repo: ICashRegisterRepository):
        self.repo = repo
    async def __call__(self, id: str, business_id: str, closing_amount: float, closed_at: datetime) -> CashRegister:
        cr = await self.repo.get_by_id(id, business_id)
        cr.closing_amount = closing_amount
        cr.closed_at = closed_at
        return await self.repo.update(cr)

class GetCurrentRegister:
    def __init__(self, repo: ICashRegisterRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> CashRegister:
        registers = await self.repo.get_all(business_id)
        abiertas = [r for r in registers if r.status == "abierta"]
        return abiertas[0] if abiertas else None
