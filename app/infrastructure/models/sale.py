import uuid
from sqlalchemy import String, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import PaymentMethod

class Sale(Base):
    __tablename__ = "sale"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("worker.id"), nullable=True)
    promotion_id: Mapped[str] = mapped_column(String(36), ForeignKey("promotion.id"), nullable=True)
    cash_register_id: Mapped[str] = mapped_column(String(36), ForeignKey("cash_register.id"), nullable=False)
    subtotal: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    discount: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    total: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    cash_register = relationship("CashRegister", back_populates="sales")
    worker = relationship("Worker", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale")
    participations = relationship("WorkerParticipation", back_populates="sale")
