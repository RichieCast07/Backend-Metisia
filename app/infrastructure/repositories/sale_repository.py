from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.sale import Sale as SaleEntity
from app.domain.entities.sale_item import SaleItem as SaleItemEntity
from app.domain.entities.worker_participation import WorkerParticipation as WorkerParticipationEntity
from app.domain.repositories.sale_repository import ISaleRepository
from app.infrastructure.models.sale import Sale as SaleModel
from app.infrastructure.models.sale_item import SaleItem as SaleItemModel
from app.infrastructure.models.worker_participation import WorkerParticipation as WorkerParticipationModel
from app.infrastructure.models.product_ingredient import ProductIngredient as ProductIngredientModel
from app.infrastructure.models.ingredient import Ingredient as IngredientModel
from app.infrastructure.models.ingredient_movement import IngredientMovement as IngredientMovementModel
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime

class SaleRepository(ISaleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[SaleEntity]:
        stmt = select(SaleModel).where(SaleModel.id == id, SaleModel.business_id == business_id)
        result = await self.session.execute(stmt)
        sale = result.scalar_one_or_none()
        return SaleEntity(**sale.__dict__) if sale else None

    async def get_all(self, business_id: str) -> List[SaleEntity]:
        stmt = select(SaleModel).where(SaleModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [SaleEntity(**s.__dict__) for s in result.scalars().all()]

    async def create(self, entity: SaleEntity) -> SaleEntity:
        sale = SaleModel(**entity.__dict__)
        self.session.add(sale)
        await self.session.commit()
        await self.session.refresh(sale)
        return SaleEntity(**sale.__dict__)

    async def update(self, entity: SaleEntity) -> SaleEntity:
        await self.session.execute(update(SaleModel).where(SaleModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(SaleModel).where(SaleModel.id == id, SaleModel.business_id == business_id))
        await self.session.commit()
        return True

    async def create_with_items(self, sale: SaleEntity, items: List[SaleItemEntity], participations: List[WorkerParticipationEntity]) -> SaleEntity:
        async with self.session.begin():
            # 1. Por cada SaleItem, obtener la receta del producto (ProductIngredient)
            for item in items:
                stmt = select(ProductIngredientModel).where(ProductIngredientModel.product_id == item.product_id)
                result = await self.session.execute(stmt)
                recipe = result.scalars().all()
                # 2. Por cada ingrediente en la receta:
                for pi in recipe:
                    stmt_ing = select(IngredientModel).where(IngredientModel.id == pi.ingredient_id)
                    ing_result = await self.session.execute(stmt_ing)
                    ingredient = ing_result.scalar_one()
                    quantity_needed = pi.quantity * item.quantity
                    if ingredient.stock < quantity_needed:
                        raise ValueError(f"Stock insuficiente para ingrediente {ingredient.name}")
                    # b. Descontar stock
                    ingredient.stock -= quantity_needed
                    self.session.add(ingredient)
                    # c. Crear IngredientMovement tipo SALIDA
                    movement = IngredientMovementModel(
                        id=None,
                        business_id=sale.business_id,
                        ingredient_id=ingredient.id,
                        type="salida",
                        quantity=quantity_needed,
                        reason="Venta automática",
                        date=datetime.utcnow()
                    )
                    self.session.add(movement)
            # 3. Insertar Sale
            sale_model = SaleModel(**sale.__dict__)
            self.session.add(sale_model)
            await self.session.flush()
            # 4. Insertar SaleItems
            for item in items:
                item_model = SaleItemModel(**item.__dict__, sale_id=sale_model.id)
                self.session.add(item_model)
            # 5. Insertar WorkerParticipations
            for part in participations:
                part_model = WorkerParticipationModel(**part.__dict__, sale_id=sale_model.id)
                self.session.add(part_model)
        await self.session.commit()
        await self.session.refresh(sale_model)
        return SaleEntity(**sale_model.__dict__)
