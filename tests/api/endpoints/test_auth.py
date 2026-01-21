from httpx import AsyncClient
from fastapi import status
from core.settings import settings
from unittest.mock import patch
import pytest


@pytest.mark.integration
async def test_create_account_success(client: AsyncClient):
    with patch('api.endpoints.auth.send_email.delay') as mock_delay:
        response = await client.post(
            f'{settings.API_PREFIX}/auth/create_account',
            json={
                'name': 'João',
                'email': 'joao@genericemail.com',
                'password': '#Apipadoxandaonaosobemais1'
            }
        )

        body = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in body
        assert isinstance(body['id'], int)
        assert body['name'] == 'João'
        assert body['email'] == 'joao@genericemail.com'
        mock_delay.assert_called_with('João', 'joao@genericemail.com')


@pytest.mark.integration
@pytest.mark.parametrize(
    'email',
    [
        'joaogenericemail.com',
        'joaogenericemailcom',
        'joao@genericemail',
        'joao@genericemail.com.',
        '.joao@genericemail.com'
    ]
)
async def test_create_account_invalid_email(client: AsyncClient, email):
    response = await client.post(
        f'{settings.API_PREFIX}/auth/create_account',
        json={
            'name': 'João',
            'email': email,
            'password': '#Apipadoxandaonaosobemais1'
        }
    )

    body = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert 'detail' in body
    assert 'loc' in body['detail'][0]
    assert body['detail'][0]['loc'] == ['body', 'email']
    assert body['detail'][0]['type'] == 'value_error'


@pytest.mark.integration
@pytest.mark.parametrize(
    'password, expected_error_hint', [
        ('#Apipadoxandaonaosobemais', 'número'),
        ('Apipadoxandaonaosobemais1', 'caractere especial'),
        ('#pipadoxandaonaosobemais1', 'letra maiúscula'),
        ('#APIPADOXANDAONAOSOBEMAIS1', 'letra minúscula'),
        ('#Aaaaa1', '8')
    ]
)
async def test_create_account_invalid_password(client: AsyncClient, password: str, expected_error_hint: str):
    response = await client.post(
        f'{settings.API_PREFIX}/auth/create_account',
        json={
            'name': 'João',
            'email': 'joao@genericemail.com',
            'password': password
        }
    )

    body = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert 'detail' in body
    assert 'loc' in body['detail'][0]
    assert body['detail'][0]['loc'] == ['body', 'password']
    assert 'detail' in body
    assert 'loc' in body['detail'][0]
    assert body['detail'][0]['type'] == 'value_error'

    assert expected_error_hint.lower() in str(body['detail'][0]['msg']).lower()


@pytest.mark.integration_duplicate_email
async def test_create_account_duplicate_email(client: AsyncClient):
    await client.post(
        f'{settings.API_PREFIX}/auth/create_account',
        json={
            'name': 'João',
            'email': 'joao@genericemail.com',
            'password': '#Apipadoxandaonaosobemais1'
        }
    )

    response = await client.post(
        f'{settings.API_PREFIX}/auth/create_account',
        json={
            'name': 'Felipe',
            'email': 'joao@genericemail.com',
            'password': '#Apipadoxandaonaosobemais1'
        }
    )
    body = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT
    assert 'detail' in body
    assert isinstance(body['detail'], str) is True
