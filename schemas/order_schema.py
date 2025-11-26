from schemas.app_base_model import AppBaseModel
from pydantic import field_validator


class OrderSchema(AppBaseModel):
    user_id: int

    @field_validator('user_id')
    def validade_user_id(cls, user_id: int) -> int:
        if user_id < 0:
            raise ValueError('ID do usuário deve ser maior que zero.')
        return user_id


class OrderResponse(OrderSchema):
    id: int
    status: str

    @field_validator('id')
    def validade_id(cls, id: int) -> int:
        if id < 0:
            raise ValueError('ID do pedido deve ser maior que zero.')
        return id
