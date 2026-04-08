from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.presentation.dependencies import get_db, get_current_user, get_product_repository
from app.presentation.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.application.use_cases.product_use_cases import (
    CreateProduct, UpdateProduct, DeleteProduct, ListProducts, GetProduct
)
from app.domain.entities.product import Product
from app.domain.entities.user import User
import uuid
from datetime import datetime

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    repo=Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = ListProducts(repo)
    return await use_case(current_user.id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    body: ProductCreate,
    repo=Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    entity = Product(
        id=str(uuid.uuid4()),
        business_id=current_user.id,
        name=body.name,
        description=body.description,
        price=body.price,
        category=body.category,
        image_url=body.image_url,
        is_active=body.is_active if body.is_active is not None else True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    use_case = CreateProduct(repo)
    return await use_case(entity)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    repo=Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = GetProduct(repo)
    product = await use_case(product_id, current_user.id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    body: ProductUpdate,
    repo=Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    get_use_case = GetProduct(repo)
    existing = await get_use_case(product_id, current_user.id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    updated = Product(
        id=existing.id,
        business_id=existing.business_id,
        name=body.name if body.name is not None else existing.name,
        description=body.description if body.description is not None else existing.description,
        price=body.price if body.price is not None else existing.price,
        category=body.category if body.category is not None else existing.category,
        image_url=body.image_url if body.image_url is not None else existing.image_url,
        is_active=body.is_active if body.is_active is not None else existing.is_active,
        created_at=existing.created_at,
        updated_at=datetime.utcnow(),
    )
    use_case = UpdateProduct(repo)
    return await use_case(updated)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    repo=Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteProduct(repo)
    deleted = await use_case(product_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
