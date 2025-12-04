from schemas.app_base_model import AppBaseModel
from pydantic import field_validator
from decimal import Decimal
from schemas.order_status_enum import OrderStatusEnum
from schemas.order_item_schema import OrderItemResponseSchema, OrderItemNoOrderId


class OrderResponseSchema(AppBaseModel):
    id: int
    user_id: int
    status: OrderStatusEnum
    total_price: Decimal

    @field_validator('id')
    def validade_id(cls, id: int) -> int:
        if id < 0:
            raise ValueError('ID do pedido deve ser maior que zero.')
        return id

    @field_validator('user_id')
    def validade_user_id(cls, user_id: int) -> int:
        if user_id < 0:
            raise ValueError('ID do usuário deve ser maior que zero.')
        return user_id

    @field_validator('total_price')
    def validate_total_price(cls, total_price: Decimal) -> Decimal:
        if total_price < 0:
            raise ValueError('O valor total do pedido não pode ser negativo.')
        return total_price


class OrderWithItemsResponse(OrderResponseSchema):
    order_items: list[OrderItemNoOrderId]
