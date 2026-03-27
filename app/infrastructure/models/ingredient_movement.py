import uuid
from sqlalchemy import String, DECIMAL, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import IngredientMovementType

class IngredientMovement(Base):
    __tablename__ = "ingredient_movement"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    ingredient_id: Mapped[str] = mapped_column(String(36), ForeignKey("ingredient.id"), nullable=False)
    type: Mapped[IngredientMovementType] = mapped_column(Enum(IngredientMovementType), nullable=False)
    quantity: Mapped[float] = mapped_column(DECIMAL(10,3), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    ingredient = relationship("Ingredient", back_populates="movements")
