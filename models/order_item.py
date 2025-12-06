from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from core.settings import settings as stt
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

if TYPE_CHECKING:
    from models.order import Order


class OrderItem(stt.DBBaseModel):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)

    flavor: Mapped[str] = mapped_column(String(100), nullable=False)

    size: Mapped[str] = mapped_column(String(50), nullable=False)

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00)

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    order: Mapped['Order'] = relationship(
        back_populates='order_items', lazy='joined')

    def __repr__(self):
        return f'Flavor: {self.flavor}\nsize: {self.size}'
