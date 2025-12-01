from schemas.app_base_model import AppBaseModel
from pydantic import field_validator


class OrderResponse(AppBaseModel):
    id: int
    user_id: int
    status: str

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
