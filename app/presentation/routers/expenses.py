from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.dependencies import get_current_user, get_expense_repository
from app.presentation.schemas.expense import ExpenseCreate, ExpenseResponse
from app.application.use_cases.expense_use_cases import CreateExpense, ListExpenses
from app.domain.entities.expense import Expense
from app.domain.entities.user import User
import uuid
from datetime import datetime

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=List[ExpenseResponse])
async def list_expenses(
    repo=Depends(get_expense_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = ListExpenses(repo)
    return await use_case(current_user.id)


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    body: ExpenseCreate,
    repo=Depends(get_expense_repository),
    current_user: User = Depends(get_current_user),
):
    entity = Expense(
        id=str(uuid.uuid4()),
        business_id=current_user.id,
        description=body.description,
        amount=body.amount,
        category=body.category,
        date=body.date,
        created_at=datetime.utcnow(),
    )
    use_case = CreateExpense(repo)
    return await use_case(entity)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str,
    repo=Depends(get_expense_repository),
    current_user: User = Depends(get_current_user),
):
    expenses = await ListExpenses(repo)(current_user.id)
    existing = next((e for e in expenses if e.id == expense_id), None)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")
    deleted = await repo.delete(expense_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")
