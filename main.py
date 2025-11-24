from models import _all_models
from fastapi import FastAPI
from core.settings import settings
from api.api import api_router

app = FastAPI()
app.include_router(router=api_router, prefix=settings.API_PREFIX)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
