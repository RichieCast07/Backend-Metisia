import uuid
from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.models.base import Base

class ProductIngredient(Base):
    __tablename__ = "product_ingredient"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("product.id"), nullable=False)
    ingredient_id: Mapped[str] = mapped_column(String(36), ForeignKey("ingredient.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(DECIMAL(10,4), nullable=False)

    product = relationship("Product", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="product_ingredients")
