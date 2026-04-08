from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.dependencies import get_current_user, get_ingredient_repository, get_ingredient_movement_repository
from app.presentation.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.application.use_cases.ingredient_use_cases import (
    CreateIngredient, UpdateIngredient, DeleteIngredient, ListIngredients
)
from app.domain.entities.ingredient import Ingredient
from app.domain.entities.user import User
import uuid
from datetime import datetime

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=List[IngredientResponse])
async def list_ingredients(
    repo=Depends(get_ingredient_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = ListIngredients(repo)
    return await use_case(current_user.id)


@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    body: IngredientCreate,
    repo=Depends(get_ingredient_repository),
    current_user: User = Depends(get_current_user),
):
    entity = Ingredient(
        id=str(uuid.uuid4()),
        business_id=current_user.id,
        name=body.name,
        unit=body.unit,
        stock=body.stock,
        min_stock=body.min_stock,
        unit_cost=body.unit_cost,
        supplier=body.supplier,
        updated_at=datetime.utcnow(),
    )
    use_case = CreateIngredient(repo)
    return await use_case(entity)


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: str,
    body: IngredientUpdate,
    repo=Depends(get_ingredient_repository),
    current_user: User = Depends(get_current_user),
):
    ingredients = await ListIngredients(repo)(current_user.id)
    existing = next((i for i in ingredients if i.id == ingredient_id), None)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    updated = Ingredient(
        id=existing.id,
        business_id=existing.business_id,
        name=body.name if body.name is not None else existing.name,
        unit=body.unit if body.unit is not None else existing.unit,
        stock=body.stock if body.stock is not None else existing.stock,
        min_stock=body.min_stock if body.min_stock is not None else existing.min_stock,
        unit_cost=body.unit_cost if body.unit_cost is not None else existing.unit_cost,
        supplier=body.supplier if body.supplier is not None else existing.supplier,
        updated_at=datetime.utcnow(),
    )
    use_case = UpdateIngredient(repo)
    return await use_case(updated)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: str,
    repo=Depends(get_ingredient_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteIngredient(repo)
    deleted = await use_case(ingredient_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
