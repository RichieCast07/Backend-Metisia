import uuid
from sqlalchemy import String, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import CashRegisterStatus

class CashRegister(Base):
    __tablename__ = "cash_register"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    status: Mapped[CashRegisterStatus] = mapped_column(Enum(CashRegisterStatus), nullable=False)
    opening_amount: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    closing_amount: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=True)
    opened_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    opened_by: Mapped[str] = mapped_column(String(36), nullable=False)

    business = relationship("User", back_populates="cash_registers")
    histories = relationship("CashRegisterHistory", back_populates="cash_register")
    sales = relationship("Sale", back_populates="cash_register")
