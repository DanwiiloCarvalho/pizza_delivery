from common.celery_app import celery_app


@celery_app.task
def send_email(email: str):
    return f'Email enviado para o endereço {email}'
