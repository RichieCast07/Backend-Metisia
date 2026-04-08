from app.database import AsyncSessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.config import settings
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.product_repository import ProductRepository
from app.infrastructure.repositories.ingredient_repository import IngredientRepository
from app.infrastructure.repositories.product_ingredient_repository import ProductIngredientRepository
from app.infrastructure.repositories.ingredient_movement_repository import IngredientMovementRepository
from app.infrastructure.repositories.promotion_repository import PromotionRepository
from app.infrastructure.repositories.cash_register_repository import CashRegisterRepository
from app.infrastructure.repositories.worker_repository import WorkerRepository
from app.infrastructure.repositories.sale_repository import SaleRepository
from app.infrastructure.repositories.expense_repository import ExpenseRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

def get_product_repository(db: AsyncSession = Depends(get_db)):
    return ProductRepository(db)

def get_ingredient_repository(db: AsyncSession = Depends(get_db)):
    return IngredientRepository(db)

def get_product_ingredient_repository(db: AsyncSession = Depends(get_db)):
    return ProductIngredientRepository(db)

def get_ingredient_movement_repository(db: AsyncSession = Depends(get_db)):
    return IngredientMovementRepository(db)

def get_promotion_repository(db: AsyncSession = Depends(get_db)):
    return PromotionRepository(db)

def get_cash_register_repository(db: AsyncSession = Depends(get_db)):
    return CashRegisterRepository(db)

def get_worker_repository(db: AsyncSession = Depends(get_db)):
    return WorkerRepository(db)

def get_sale_repository(db: AsyncSession = Depends(get_db)):
    return SaleRepository(db)

def get_expense_repository(db: AsyncSession = Depends(get_db)):
    return ExpenseRepository(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
