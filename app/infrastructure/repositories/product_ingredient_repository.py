from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.product_ingredient import ProductIngredient as ProductIngredientEntity
from app.domain.repositories.product_ingredient_repository import IProductIngredientRepository
from app.infrastructure.models.product_ingredient import ProductIngredient as ProductIngredientModel
from typing import Optional, List

class ProductIngredientRepository(IProductIngredientRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[ProductIngredientEntity]:
        stmt = select(ProductIngredientModel).join(ProductIngredientModel.product).where(ProductIngredientModel.id == id, ProductIngredientModel.product.has(business_id=business_id))
        result = await self.session.execute(stmt)
        pi = result.scalar_one_or_none()
        return ProductIngredientEntity(**pi.__dict__) if pi else None

    async def get_all(self, business_id: str) -> List[ProductIngredientEntity]:
        stmt = select(ProductIngredientModel).join(ProductIngredientModel.product).where(ProductIngredientModel.product.has(business_id=business_id))
        result = await self.session.execute(stmt)
        return [ProductIngredientEntity(**pi.__dict__) for pi in result.scalars().all()]

    async def create(self, entity: ProductIngredientEntity) -> ProductIngredientEntity:
        pi = ProductIngredientModel(**entity.__dict__)
        self.session.add(pi)
        await self.session.commit()
        await self.session.refresh(pi)
        return ProductIngredientEntity(**pi.__dict__)

    async def update(self, entity: ProductIngredientEntity) -> ProductIngredientEntity:
        await self.session.execute(update(ProductIngredientModel).where(ProductIngredientModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(ProductIngredientModel).where(ProductIngredientModel.id == id))
        await self.session.commit()
        return True
