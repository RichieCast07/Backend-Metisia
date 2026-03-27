import uuid
from sqlalchemy import String, DECIMAL, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.models.base import Base
from app.domain.entities.enums import Unit

class Ingredient(Base):
    __tablename__ = "ingredient"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[Unit] = mapped_column(Enum(Unit), nullable=False)
    stock: Mapped[float] = mapped_column(DECIMAL(10,3), nullable=False)
    min_stock: Mapped[float] = mapped_column(DECIMAL(10,3), nullable=False)
    unit_cost: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    supplier: Mapped[str] = mapped_column(String(100), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("User", back_populates="ingredients")
    product_ingredients = relationship("ProductIngredient", back_populates="ingredient")
    movements = relationship("IngredientMovement", back_populates="ingredient")
