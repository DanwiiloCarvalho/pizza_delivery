from schemas.app_base_model import AppBaseModel
from pydantic import field_validator
from pydantic import EmailStr


class BaseUserSchema(AppBaseModel):
    id: int | None = None
    name: str
    email: EmailStr

    @field_validator('name')
    def validade_name(cls, name: str) -> str:
        if not name.isalnum():
            raise ValueError(
                'Nome de usuário deve conter apenas letras e números')
        if len(name) < 3 or len(name) > 16:
            raise ValueError(
                'O nome de usuário deve ter um comprimento de 3 a 16 caracteres')
        return name


class RegisterUserSchema(BaseUserSchema):
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        if not any(char.isupper() for char in password):
            raise ValueError(
                'A senha deve conter pelo menos uma letra maiúscula')
        if not any(char.islower() for char in password):
            raise ValueError(
                'A senha deve conter pelo menos uma letra minúscula')
        if not any(char.isdigit() for char in password):
            raise ValueError('A senha deve conter pelo menos um número')
        if not any(not char.isalnum() for char in password):
            raise ValueError(
                'A senha deve conter pelo menos um caractere especial')
        return password
