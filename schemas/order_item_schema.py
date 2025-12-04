from schemas.app_base_model import AppBaseModel
from pydantic import Field
from decimal import Decimal


class OrderItemBaseSchema(AppBaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: Decimal


class OrderItemResponseSchema(OrderItemBaseSchema):
    id: int
    order_id: int


class OrderItemNoOrderId(OrderItemResponseSchema):
    order_id: int = Field(exclude=True)
