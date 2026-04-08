from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.dependencies import get_current_user, get_sale_repository
from app.presentation.schemas.sale import SaleCreate, SaleResponse
from app.application.use_cases.sale_use_cases import CreateSale, ListSales, GetSale
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.worker_participation import WorkerParticipation
from app.domain.entities.user import User
import uuid
from datetime import datetime

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/", response_model=List[SaleResponse])
async def list_sales(
    repo=Depends(get_sale_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = ListSales(repo)
    return await use_case(current_user.id)


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: str,
    repo=Depends(get_sale_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = GetSale(repo)
    sale = await use_case(sale_id, current_user.id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")
    return sale


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    body: SaleCreate,
    repo=Depends(get_sale_repository),
    current_user: User = Depends(get_current_user),
):
    sale_id = str(uuid.uuid4())
    sale = Sale(
        id=sale_id,
        business_id=current_user.id,
        worker_id=body.worker_id,
        promotion_id=body.promotion_id,
        cash_register_id=body.cash_register_id,
        subtotal=body.subtotal,
        discount=body.discount,
        total=body.total,
        payment_method=body.payment_method,
        notes=body.notes,
        created_at=datetime.utcnow(),
    )
    items = [
        SaleItem(
            id=str(uuid.uuid4()),
            sale_id=sale_id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.subtotal,
        )
        for item in body.items
    ]
    participations = [
        WorkerParticipation(
            id=str(uuid.uuid4()),
            sale_id=sale_id,
            worker_id=p.worker_id,
            percentage=p.percentage,
        )
        for p in (body.participations or [])
    ]
    use_case = CreateSale(repo)
    return await use_case(sale, items, participations)
