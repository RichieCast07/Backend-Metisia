from app.domain.repositories.expense_repository import IExpenseRepository
from app.domain.entities.expense import Expense
from typing import List
from datetime import datetime

class CreateExpense:
    def __init__(self, repo: IExpenseRepository):
        self.repo = repo
    async def __call__(self, expense: Expense) -> Expense:
        return await self.repo.create(expense)

class ListExpenses:
    def __init__(self, repo: IExpenseRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> List[Expense]:
        return await self.repo.get_all(business_id)

class GetExpensesByPeriod:
    def __init__(self, repo: IExpenseRepository):
        self.repo = repo
    async def __call__(self, start_date: datetime, end_date: datetime, business_id: str) -> List[Expense]:
        all_expenses = await self.repo.get_all(business_id)
        return [e for e in all_expenses if start_date <= e.date <= end_date]
