from schemas.app_base_model import AppBaseModel


class AccessTokenSchema(AppBaseModel):
    access_token: str


class TokenSchema(AccessTokenSchema):
    refresh_token: str
    token_type: str


class TokenDataSchema(AppBaseModel):
    user_id: int | None = None
