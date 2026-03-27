import uuid
from sqlalchemy import String, DECIMAL, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base

class Worker(Base):
    __tablename__ = "worker"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    daily_rate: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    hired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    business = relationship("User", back_populates="workers")
    payments = relationship("WorkerPayment", back_populates="worker")
    participations = relationship("WorkerParticipation", back_populates="worker")
    sales = relationship("Sale", back_populates="worker")
