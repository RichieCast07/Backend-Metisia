import uuid
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import BusinessType, Plan

class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    business_name: Mapped[str] = mapped_column(String(100), nullable=False)
    business_type: Mapped[BusinessType] = mapped_column(Enum(BusinessType), nullable=False)
    plan: Mapped[Plan] = mapped_column(Enum(Plan), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    products = relationship("Product", back_populates="business")
    ingredients = relationship("Ingredient", back_populates="business")
    promotions = relationship("Promotion", back_populates="business")
    cash_registers = relationship("CashRegister", back_populates="business")
    workers = relationship("Worker", back_populates="business")
    expenses = relationship("Expense", back_populates="business")
