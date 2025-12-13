from models import _all_models
from fastapi import FastAPI, __version__
from core.settings import settings
from api.api import api_router
from pathlib import Path
from fastapi.responses import HTMLResponse
from exceptions.handlers import register_exception_handlers
import sys

app = FastAPI(
    title='Desafio Pizza Delivery',
    description='Sistema de um delivery, onde um usuário poderá criar uma conta, fazer o login, criar pedidos e '
    'realizar operações que normalmente são feitas em um delivery como: criar um pedido, adicionar itens a um pedido, '
    'listar um pedido específico, listar todos os itens de um pedido, cancelar um pedido, etc.',
    version='1.0.0'
)
app.include_router(router=api_router, prefix=settings.API_PREFIX)
register_exception_handlers(app)


@app.get('/')
def root():
    html_path: str = Path('index.html').read_text('utf-8')
    html_path = html_path.replace('{__python__}', sys.version)
    html_path = html_path.replace('{__fastapi__}', __version__)
    return HTMLResponse(content=html_path)


# if __name__ == '__main__':
#     import uvicorn

#     uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
