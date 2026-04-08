from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.user import User as UserEntity
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.models.user import User as UserModel
from typing import Optional

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> Optional[UserEntity]:
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserEntity(**user.__dict__) if user else None

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserEntity(**user.__dict__) if user else None

    async def create(self, entity: UserEntity) -> UserEntity:
        user = UserModel(**entity.__dict__)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserEntity(**user.__dict__)

    async def update(self, entity: UserEntity) -> UserEntity:
        await self.session.execute(
            update(UserModel).where(UserModel.id == entity.id).values(**entity.__dict__)
        )
        await self.session.commit()
        return entity

    async def delete(self, id: str) -> bool:
        await self.session.execute(delete(UserModel).where(UserModel.id == id))
        await self.session.commit()
        return True
