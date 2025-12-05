from fastapi import APIRouter
from api.endpoints import orders, auth, users

api_router = APIRouter()

api_router.include_router(router=orders.router,
                          prefix='/orders', tags=['Pedidos'])

api_router.include_router(
    router=auth.router, prefix='/auth', tags=['Autenticação'])

api_router.include_router(
    router=users.router, prefix='/users', tags=['Usuários'])
