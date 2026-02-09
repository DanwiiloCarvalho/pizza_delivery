from locust import HttpUser, between, task
from core.settings import settings
from fastapi import status
import uuid


class ApiUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_user(self):
        payload = {
            'name': 'João',
            'email': f'joao_success_{uuid.uuid4().hex[:10]}@genericemail.com',
            'password': '#Apipadoxandaonaosobemais1'
        }

        headers = {
            "Content-Type": "application/json"
        }

        with self.client.post(
            f'{settings.API_PREFIX}/auth/create_account',
            json=payload,
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code != status.HTTP_201_CREATED:
                response.failure(
                    f'Erro ao criar um usuário: {response.status_code}')
