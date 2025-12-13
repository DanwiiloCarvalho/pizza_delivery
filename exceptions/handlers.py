from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from socket import gaierror


def database_unavailable_handler(request: Request, exc: Exception):
    """Handler para exceções de conexão com o banco de dados."""
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content='Serviço de banco de dados indisponível no momento.')


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(gaierror, database_unavailable_handler)
    app.add_exception_handler(ConnectionRefusedError,
                              database_unavailable_handler)
