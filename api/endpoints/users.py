from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.deps import get_session, get_current_user
from models.user import User
from schemas.order_schema import OrderWithItemsResponse

router = APIRouter()


@router.get(
    '/{user_id}/orders',
    status_code=status.HTTP_200_OK,
    response_model=list[OrderWithItemsResponse],
    summary='Lista todos os pedidos de um usuário',
    description='Lista todos os pedidos de um usuário de ID especificado.'
)
async def get_orders(user_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    if user_id == current_user.id:
        return current_user.orders
    if current_user.admin:
        query = select(User).filter(User.id == user_id)
        user: User = (await db.execute(query)).unique().scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Usuário de ID = {user_id} não encontrado')

        return user.orders
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Você não está autorizado')
