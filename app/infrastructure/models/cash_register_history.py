import uuid
from sqlalchemy import String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base

class CashRegisterHistory(Base):
    __tablename__ = "cash_register_history"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cash_register_id: Mapped[str] = mapped_column(String(36), ForeignKey("cash_register.id"), nullable=False)
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    opening_amount: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    closing_amount: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=True)
    total_sales: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    total_expenses: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    difference: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    cash_register = relationship("CashRegister", back_populates="histories")
