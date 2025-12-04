from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc
from core.deps import get_session, get_current_user
from schemas.order_schema import OrderResponseSchema, OrderWithItemsResponse
from schemas.order_item_schema import OrderItemResponseSchema, OrderItemBaseSchema
from schemas.order_status_enum import OrderStatusEnum
from models.order import Order
from models.user import User
from models.order_item import OrderItem

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponseSchema,
    summary='Cria um pedido',
    description='Cria um pedido de usuário no Pizza Delivery',
    response_description='Retorna o pedido cadastrado'
)
async def create_order(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    order = Order(user_id=current_user.id)

    db.add(order)
    await db.commit()

    return order


@router.patch(
    '/{order_id}',
    status_code=status.HTTP_200_OK,
    response_model=OrderResponseSchema,
    summary='Cancela um pedido',
    description='Cancela um pedido do usuário no Pizza Delivery',
    response_description='Retorna o pedido cancelado'
)
async def cancel_order(order_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(Order).filter(Order.id == order_id)
    order: Order = (await db.execute(query)).unique().scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Pedido de ID {order_id} não encontrado.')
    if not current_user.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Você não tem autorização para cancelar o pedido')

    order.status = OrderStatusEnum.CANCELED
    await db.commit()

    return order


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[OrderWithItemsResponse],
    summary='Lista todos os pedidos',
    description='Lista todos os pedidos do Pizza Delivery. Rota disponível apenas para usuários administrativos',
    response_description='Retorna uma listagem com todos os pedidos do Pizza Delivery'
)
async def get_orders(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Usuário não autorizado')

    query = select(Order).order_by(asc(Order.id))
    orders: list[Order] = (await db.execute(query)).unique().scalars().all()

    return orders


@router.post(
    '/{order_id}/items',
    status_code=status.HTTP_201_CREATED,
    response_model=OrderItemResponseSchema,
    summary='Adiciona um novo item ao pedido',
    description='Adiciona um novo item ao pedido'
)
async def add_order_item(order_id: int, item: OrderItemBaseSchema, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(Order).filter(Order.id == order_id)
    order: Order = (await db.execute(query)).unique().scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Pedido de ID {order_id} não encontrado.')
    if not current_user.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Você não tem autorização para adicionar um item ao pedido')
    if order.status == OrderStatusEnum.PENDING:
        new_item = OrderItem(
            quantity=item.quantity,
            flavor=item.flavor,
            size=item.size,
            unit_price=item.unit_price,
            order_id=order_id
        )
        order.order_items.append(new_item)
        order.calculate_total_price()
        await db.commit()

        return new_item
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f'Não é possível adicionar itens a um pedido com status {order.status}.')


@router.delete(
    '/{order_id}/items/{item_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Remove um item de um pedido',
    description='Remove um item de um pedido, especificando os IDs do pedido e do item'
)
async def delete_order_item(order_id: int, item_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(OrderItem).filter(OrderItem.id == item_id)
    order_item: OrderItem = (await db.execute(query)).unique().scalar_one_or_none()

    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Item de ID {item_id} não encontrado.')
    if order_item.order_id != order_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'O item especificado não pertence ao pedido de ID = {order_id}')

    if not current_user.admin and order_item.order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Você não tem autorização para adicionar o item ao pedido')

    order = order_item.order
    await db.delete(order_item)
    await db.commit()
    await db.refresh(order)
    order.calculate_total_price()
    await db.commit()


@router.patch(
    '/{order_id}/complete',
    status_code=status.HTTP_200_OK,
    response_model=OrderResponseSchema,
    summary='Finaliza um pedido',
    description='Finaliza de um pedido, ou seja, altera o status para FINALIZADO de um pedido com ID especificado'
)
async def complete_order(order_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(Order).filter(Order.id == order_id)
    order: Order = (await db.execute(query)).unique().scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Pedido de ID = {order_id} não encontrado')
    if not current_user.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Você não tem autorização para finalizar o pedido')
    if order.status == OrderStatusEnum.CANCELED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Não foi possível finalizar o pedido de ID = {order.id}. Pedido encontra-se cancelado')
    order.status = OrderStatusEnum.COMPLETED
    await db.commit()

    return order
