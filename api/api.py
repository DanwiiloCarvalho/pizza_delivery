from fastapi import APIRouter
from api.endpoints import orders

api_router = APIRouter()

api_router.include_router(router=orders.router,
                          prefix='/orders', tags=['Pedidos'])
