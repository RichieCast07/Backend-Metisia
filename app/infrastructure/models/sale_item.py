import uuid
from sqlalchemy import String, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.models.base import Base

class SaleItem(Base):
    __tablename__ = "sale_item"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sale_id: Mapped[str] = mapped_column(String(36), ForeignKey("sale.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("product.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    subtotal: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")
