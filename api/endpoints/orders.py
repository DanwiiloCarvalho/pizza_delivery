from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from schemas.order_schema import OrderSchema, OrderResponse
from models.order import Order
from models.user import User

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
    summary='Cria um pedido',
    description='Cria um pedido de usuário no Pizza Delivery',
    response_description='Retorna o pedido cadastrado'
)
async def create_order(new_order: OrderSchema, db: AsyncSession = Depends(get_session)):
    query = select(User).filter(User.id == new_order.user_id)
    user_found = (await db.execute(query)).unique().scalar_one_or_none()

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Usuário com ID {new_order.user_id} não encontrado.')

    order = Order(user_id=new_order.user_id)
    db.add(order)
    await db.commit()

    return order
