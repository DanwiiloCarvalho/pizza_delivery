from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

broker_url: str = os.getenv(key='CELERY_BROKER_URL')
backend_url: str = os.getenv(key='CELERY_RESULT_BACKEND')

celery_app = Celery(
    'pizza_delivery',
    broker=broker_url,
    include=['common.tasks'],
    backend=backend_url
)
