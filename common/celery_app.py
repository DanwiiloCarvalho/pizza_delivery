from celery import Celery

celery_app = Celery(
    'pizza_delivery',
    broker='amqp://guest:guest@rabbitmq:5672',
    include=['common.tasks']
)
