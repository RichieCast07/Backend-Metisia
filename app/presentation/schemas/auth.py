from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    business_name: str
    business_type: str
    plan: str

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
