from schemas.app_base_model import AppBaseModel


class TokenSchema(AppBaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenDataSchema(AppBaseModel):
    user_id: int | None = None
