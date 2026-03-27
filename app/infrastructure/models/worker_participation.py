import uuid
from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.models.base import Base

class WorkerParticipation(Base):
    __tablename__ = "worker_participation"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sale_id: Mapped[str] = mapped_column(String(36), ForeignKey("sale.id"), nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("worker.id"), nullable=False)
    percentage: Mapped[float] = mapped_column(DECIMAL(5,2), nullable=False)

    sale = relationship("Sale", back_populates="participations")
    worker = relationship("Worker", back_populates="participations")
