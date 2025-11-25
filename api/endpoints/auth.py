from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.deps import get_session
from schemas.user_schema import RegisterUserSchema, BaseUserSchema
from models.user import User
from core.security import generate_hash

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
