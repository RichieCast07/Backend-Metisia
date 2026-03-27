from app.domain.repositories.user_repository import IUserRepository
from app.domain.entities.user import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def __call__(self, user_data: dict) -> User:
        # Validar email único
        users = await self.repo.get_all(user_data["id"])
        if any(u.email == user_data["email"] for u in users):
            raise ValueError("Email ya registrado")
        user_data["password_hash"] = pwd_context.hash(user_data.pop("password"))
        user = User(**user_data)
        return await self.repo.create(user)

class LoginUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def __call__(self, email: str, password: str) -> str:
        users = await self.repo.get_all("")
        user = next((u for u in users if u.email == email), None)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("Credenciales inválidas")
        data = {"user_id": user.id, "business_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)}
        return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
