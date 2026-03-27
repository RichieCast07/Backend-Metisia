import uuid
from sqlalchemy import String, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import WorkerPaymentType

class WorkerPayment(Base):
    __tablename__ = "worker_payment"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("worker.id"), nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    type: Mapped[WorkerPaymentType] = mapped_column(Enum(WorkerPaymentType), nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    worker = relationship("Worker", back_populates="payments")
