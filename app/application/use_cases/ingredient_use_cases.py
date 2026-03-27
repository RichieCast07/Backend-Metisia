from app.domain.repositories.ingredient_repository import IIngredientRepository
from app.domain.entities.ingredient import Ingredient
from typing import List

class CreateIngredient:
    def __init__(self, repo: IIngredientRepository):
        self.repo = repo
    async def __call__(self, ingredient: Ingredient) -> Ingredient:
        return await self.repo.create(ingredient)

class UpdateIngredient:
    def __init__(self, repo: IIngredientRepository):
        self.repo = repo
    async def __call__(self, ingredient: Ingredient) -> Ingredient:
        return await self.repo.update(ingredient)

class DeleteIngredient:
    def __init__(self, repo: IIngredientRepository):
        self.repo = repo
    async def __call__(self, id: str, business_id: str) -> bool:
        return await self.repo.delete(id, business_id)

class ListIngredients:
    def __init__(self, repo: IIngredientRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> List[Ingredient]:
        return await self.repo.get_all(business_id)

class ListLowStockIngredients:
    def __init__(self, repo: IIngredientRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> List[Ingredient]:
        all_ingredients = await self.repo.get_all(business_id)
        return [i for i in all_ingredients if i.stock <= i.min_stock]
