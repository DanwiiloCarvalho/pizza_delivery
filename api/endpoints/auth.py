from fastapi import APIRouter, Depends, HTTPException, Cookie, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.deps import get_session, get_current_user
from core.security import generate_hash
from schemas.user_schema import RegisterUserSchema, BaseUserSchema
from schemas.login_schema import LoginSchema
from schemas.token_schema import TokenSchema, AccessTokenSchema
from models.user import User
from core.authentication import create_token, authenticate_user
from core.settings import settings as stt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated

router = APIRouter()


@router.post(
    '/create_account',
    status_code=status.HTTP_201_CREATED,
    response_model=BaseUserSchema,
    summary='Cria um usuário',
    description='Cria um conta de usuário no Pizza Delivery',
    response_description='Retorna o id, nome do usuário e e-mail cadastrado'
)
async def create_account(new_user: RegisterUserSchema, db: AsyncSession = Depends(get_session)):
    query = select(User).filter(User.email == new_user.email)
    result = await db.execute(query)
    email_exists = result.scalar()

    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='E-mail de usuário já cadastrado.')

    password: str = generate_hash(new_user.password)

    user: User = User(
        name=new_user.name,
        email=new_user.email,
        password=password,
        active=True
    )

    db.add(user)
    await db.commit()
    return user


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
    summary='Faz o login do usuário',
    description='Realiza a autenticação do usuário através de e-mail e senha, devolvendo um access token e um refresh token logo em seguida.',
    response_description='Retorna um access token, um refresh token e o tipo dos tokens.'
)
async def login(login: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_session)):
    user_found = await authenticate_user(
        db=db, username=login.username, password=login.password)

    payload_data = {
        "sub": str(user_found.id),
        "email": user_found.email,
        "iat": int(datetime.now(tz=ZoneInfo("America/Sao_Paulo")).timestamp())
    }
    access_token_expires = timedelta(
        minutes=int(stt.ACCESS_TOKEN_EXPIRE_MINUTES))

    refresh_token_expires = timedelta(days=int(stt.REFRESH_TOKEN_EXPIRE_DAYS))

    access_token: str = create_token(
        data=payload_data, expires_delta=access_token_expires)

    refresh_token: str = create_token(
        data=payload_data, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post(
    '/refresh',
    response_model=AccessTokenSchema,
    summary='Gera um novo access token',
    description='Gera um novo access token para utilização das rotas protegidas',
    response_description='Retorna um access token e o tipo do token'
)
async def refresh_access_token(refresh_token: str = Cookie(None), db: AsyncSession = Depends(get_session)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token ausente.')

    user_found = await get_current_user(refresh_token, db=db)

    payload_data = {
        "sub": str(user_found.id),
        "email": user_found.email,
        "iat": int(datetime.now(tz=ZoneInfo("America/Sao_Paulo")).timestamp())
    }

    access_token_expires = timedelta(
        minutes=int(stt.ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = create_token(
        data=payload_data, expires_delta=access_token_expires)

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
