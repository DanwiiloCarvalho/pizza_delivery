from common.celery_app import celery_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path
import os
import smtplib

load_dotenv()
email_user: str = os.getenv(key='EMAIL_USER')
email_password: str = os.getenv(key='EMAIL_PASSWORD')
smtp_host: str = os.getenv(key='SMTP_HOST')
smtp_port: str = os.getenv(key='SMTP_PORT')


@celery_app.task
def send_email(username: str, email: str):
    email_msg = MIMEMultipart('alternative')

    email_msg["From"] = email_user
    email_msg["To"] = email
    email_msg["Subject"] = "Teste de email com Python"
    welcome_html = Path('common/welcome.html').read_text(encoding='utf-8')
    welcome_html = welcome_html.replace('{username}', username)

    email_msg.attach(MIMEText(welcome_html, 'html', 'utf-8'))

    with smtplib.SMTP(host=smtp_host, port=smtp_port) as server:
        server.starttls()
        server.login(user=email_user,
                     password=email_password)
        server.send_message(email_msg)

    return f'E-mail de boas-vindas enviado com sucesso para {email}'
