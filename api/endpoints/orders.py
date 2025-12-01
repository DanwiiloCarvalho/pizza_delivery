from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session, get_current_user
from schemas.order_schema import OrderResponse
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
async def create_order(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    order = Order(user_id=current_user.id)

    db.add(order)
    await db.commit()

    return order
