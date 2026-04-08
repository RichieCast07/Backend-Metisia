from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.presentation.dependencies import get_db, get_current_user
from app.presentation.schemas.auth import AuthRegisterRequest, AuthResponse
from app.application.use_cases.auth_use_cases import RegisterUser, LoginUser
from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.entities.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(body: AuthRegisterRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = RegisterUser(repo)
    try:
        await use_case({
            "name": body.name,
            "email": body.email,
            "password": body.password,
            "business_name": body.business_name,
            "business_type": body.business_type,
        })
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    login_use_case = LoginUser(repo)
    token = await login_use_case(body.email, body.password)
    return AuthResponse(access_token=token)


@router.post("/login", response_model=AuthResponse)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = LoginUser(repo)
    try:
        token = await use_case(form.username, form.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthResponse(access_token=token)


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "business_name": current_user.business_name,
        "business_type": current_user.business_type,
        "plan": current_user.plan,
    }
