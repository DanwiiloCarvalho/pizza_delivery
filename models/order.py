from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Numeric, ForeignKey
# from sqlalchemy_utils.types import ChoiceType
from core.settings import settings as stt
from decimal import Decimal
from typing import TYPE_CHECKING

# ORDER_STATUS = [
#     ('PENDENTE', 'PENDENTE'),
#     ('CANCELADO', 'CANCELADO'),
#     ('FINALIZADO', 'FINALIZADO')
# ]

if TYPE_CHECKING:
    from models.user import User
    from models.order_item import OrderItem


class Order(stt.DBBaseModel):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    # pendente, cancelado, finalizado
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default='PENDENTE')

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00)

    # Relationships
    user: Mapped['User'] = relationship(back_populates='orders', lazy='joined')
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order', lazy='joined')

    def __repr__(self):
        return f'Status: {self.status}\nusuário: {self.user.name}'
