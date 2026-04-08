from app.domain.repositories.user_repository import IUserRepository
from app.domain.entities.user import User
from app.domain.entities.enums import Plan
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def __call__(self, user_data: dict) -> User:
        existing = await self.repo.find_by_email(user_data["email"])
        if existing:
            raise ValueError("Email ya registrado")
        user_data["password_hash"] = pwd_context.hash(user_data.pop("password"))
        user_data["id"] = str(uuid.uuid4())
        user_data["created_at"] = datetime.utcnow()
        user_data["last_login_at"] = None
        user_data["plan"] = Plan.basico
        user = User(**user_data)
        return await self.repo.create(user)

class LoginUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def __call__(self, email: str, password: str) -> str:
        user = await self.repo.find_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("Credenciales inválidas")
        user.last_login_at = datetime.utcnow()
        await self.repo.update(user)
        payload = {
            "user_id": user.id,
            "business_id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
