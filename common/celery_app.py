from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

broker_url: str = os.getenv(key='CELERY_BROKER_URL')

celery_app = Celery(
    'pizza_delivery',
    broker=broker_url,
    include=['common.tasks']
)
