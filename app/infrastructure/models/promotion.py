import uuid
from sqlalchemy import String, DECIMAL, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import PromotionType, PromotionApplicableTo

class Promotion(Base):
    __tablename__ = "promotion"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[PromotionType] = mapped_column(Enum(PromotionType), nullable=False)
    value: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    applicable_to: Mapped[PromotionApplicableTo] = mapped_column(Enum(PromotionApplicableTo), nullable=False)
    target_id: Mapped[str] = mapped_column(String(36), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    business = relationship("User", back_populates="promotions")
