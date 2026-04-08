from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.dependencies import get_current_user, get_worker_repository
from app.presentation.schemas.worker import WorkerCreate, WorkerUpdate, WorkerResponse
from app.application.use_cases.worker_use_cases import CreateWorker, UpdateWorker, ListWorkers, RegisterPayment
from app.domain.entities.worker import Worker
from app.domain.entities.worker_payment import WorkerPayment
from app.domain.entities.user import User
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/workers", tags=["workers"])


class WorkerPaymentCreate(BaseModel):
    amount: float
    paid_at: datetime
    notes: str | None = None


@router.get("/", response_model=List[WorkerResponse])
async def list_workers(
    repo=Depends(get_worker_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = ListWorkers(repo)
    return await use_case(current_user.id)


@router.post("/", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def create_worker(
    body: WorkerCreate,
    repo=Depends(get_worker_repository),
    current_user: User = Depends(get_current_user),
):
    entity = Worker(
        id=str(uuid.uuid4()),
        business_id=current_user.id,
        name=body.name,
        role=body.role,
        phone=body.phone,
        daily_rate=body.daily_rate,
        is_active=body.is_active if body.is_active is not None else True,
        hired_at=body.hired_at,
    )
    use_case = CreateWorker(repo)
    return await use_case(entity)


@router.put("/{worker_id}", response_model=WorkerResponse)
async def update_worker(
    worker_id: str,
    body: WorkerUpdate,
    repo=Depends(get_worker_repository),
    current_user: User = Depends(get_current_user),
):
    workers = await ListWorkers(repo)(current_user.id)
    existing = next((w for w in workers if w.id == worker_id), None)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trabajador no encontrado")
    updated = Worker(
        id=existing.id,
        business_id=existing.business_id,
        name=body.name if body.name is not None else existing.name,
        role=body.role if body.role is not None else existing.role,
        phone=body.phone if body.phone is not None else existing.phone,
        daily_rate=body.daily_rate if body.daily_rate is not None else existing.daily_rate,
        is_active=body.is_active if body.is_active is not None else existing.is_active,
        hired_at=body.hired_at if body.hired_at is not None else existing.hired_at,
    )
    use_case = UpdateWorker(repo)
    return await use_case(updated)


@router.patch("/{worker_id}/toggle", response_model=WorkerResponse)
async def toggle_worker(
    worker_id: str,
    repo=Depends(get_worker_repository),
    current_user: User = Depends(get_current_user),
):
    workers = await ListWorkers(repo)(current_user.id)
    existing = next((w for w in workers if w.id == worker_id), None)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trabajador no encontrado")
    existing.is_active = not existing.is_active
    use_case = UpdateWorker(repo)
    return await use_case(existing)


@router.post("/{worker_id}/payments", status_code=status.HTTP_201_CREATED)
async def register_payment(
    worker_id: str,
    body: WorkerPaymentCreate,
    repo=Depends(get_worker_repository),
    current_user: User = Depends(get_current_user),
):
    workers = await ListWorkers(repo)(current_user.id)
    existing = next((w for w in workers if w.id == worker_id), None)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trabajador no encontrado")
    payment = WorkerPayment(
        id=str(uuid.uuid4()),
        worker_id=worker_id,
        amount=body.amount,
        paid_at=body.paid_at,
        notes=body.notes,
    )
    use_case = RegisterPayment(repo)
    return await use_case(payment)
