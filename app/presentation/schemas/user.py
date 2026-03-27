from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.domain.entities.enums import BusinessType, Plan
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    business_name: str
    business_type: BusinessType
    plan: Plan

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    business_name: Optional[str]
    business_type: Optional[BusinessType]
    plan: Optional[Plan]

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    business_name: str
    business_type: BusinessType
    plan: Plan
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        orm_mode = True
