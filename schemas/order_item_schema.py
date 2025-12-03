from schemas.app_base_model import AppBaseModel
from decimal import Decimal


class OrderItemBaseSchema(AppBaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: Decimal


class OrderItemResponseSchema(OrderItemBaseSchema):
    id: int
    order_id: int
