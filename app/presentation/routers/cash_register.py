from fastapi import APIRouter, Depends, HTTPException, status
from app.presentation.dependencies import get_current_user, get_cash_register_repository
from app.presentation.schemas.cash_register import CashRegisterCreate, CashRegisterResponse
from app.application.use_cases.cash_register_use_cases import OpenCashRegister, CloseCashRegister, GetCurrentRegister
from app.domain.entities.cash_register import CashRegister
from app.domain.entities.enums import CashRegisterStatus
from app.domain.entities.user import User
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/cash-register", tags=["cash-register"])


class CloseRegisterBody(BaseModel):
    closing_amount: float
    closed_at: datetime


@router.get("/current", response_model=CashRegisterResponse | None)
async def get_current(
    repo=Depends(get_cash_register_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = GetCurrentRegister(repo)
    return await use_case(current_user.id)


@router.post("/open", response_model=CashRegisterResponse, status_code=status.HTTP_201_CREATED)
async def open_register(
    body: CashRegisterCreate,
    repo=Depends(get_cash_register_repository),
    current_user: User = Depends(get_current_user),
):
    entity = CashRegister(
        id=str(uuid.uuid4()),
        business_id=current_user.id,
        status=CashRegisterStatus.abierta,
        opening_amount=body.opening_amount,
        closing_amount=None,
        opened_at=body.opened_at,
        closed_at=None,
        opened_by=body.opened_by,
    )
    use_case = OpenCashRegister(repo)
    return await use_case(entity)


@router.post("/{register_id}/close", response_model=CashRegisterResponse)
async def close_register(
    register_id: str,
    body: CloseRegisterBody,
    repo=Depends(get_cash_register_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = CloseCashRegister(repo)
    result = await use_case(register_id, current_user.id, body.closing_amount, body.closed_at)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caja no encontrada")
    return result
