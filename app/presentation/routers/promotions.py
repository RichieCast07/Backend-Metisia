from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.dependencies import get_current_user, get_promotion_repository
from app.presentation.schemas.promotion import PromotionCreate, PromotionResponse
from app.application.use_cases.promotion_use_cases import (
    CreatePromotion, ListPromotions, GetPromotion, TogglePromotion, DeletePromotion
)
from app.domain.entities.promotion import Promotion
from app.domain.entities.user import User
import uuid
from datetime import datetime

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/", response_model=List[PromotionResponse])
async def list_promotions(
    repo=Depends(get_promotion_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = ListPromotions(repo)
    return await use_case(current_user.id)


@router.post("/", response_model=PromotionResponse, status_code=status.HTTP_201_CREATED)
async def create_promotion(
    body: PromotionCreate,
    repo=Depends(get_promotion_repository),
    current_user: User = Depends(get_current_user),
):
    entity = Promotion(
        id=str(uuid.uuid4()),
        business_id=current_user.id,
        name=body.name,
        type=body.type,
        value=body.value,
        applicable_to=body.applicable_to,
        target_id=body.target_id,
        is_active=body.is_active if body.is_active is not None else True,
        starts_at=body.starts_at,
        ends_at=body.ends_at,
        created_at=datetime.utcnow(),
    )
    use_case = CreatePromotion(repo)
    return await use_case(entity)


@router.patch("/{promotion_id}/toggle", response_model=PromotionResponse)
async def toggle_promotion(
    promotion_id: str,
    repo=Depends(get_promotion_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = TogglePromotion(repo)
    result = await use_case(promotion_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promoción no encontrada")
    return result


@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_promotion(
    promotion_id: str,
    repo=Depends(get_promotion_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = DeletePromotion(repo)
    deleted = await use_case(promotion_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promoción no encontrada")
