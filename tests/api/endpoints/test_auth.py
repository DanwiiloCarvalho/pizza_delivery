from httpx import AsyncClient
from fastapi import status
from core.settings import settings
from unittest.mock import patch
from hypothesis import given, strategies as st, settings as hypothesis_settings
from tests.conftest import db_session_context, client_context
from tests.factories.user_builder import UserBuilder
import string
import pytest


@hypothesis_settings(deadline=None, max_examples=20)
@pytest.mark.integration
@given(
    name=st.text(min_size=3, max_size=16,
                 alphabet=string.ascii_letters + string.digits),
    unique_id=st.uuids()
)
async def test_create_account_success(name: str, unique_id):
    email = f'joao_success_{unique_id}@genericemail.com'
    async with db_session_context() as session:
        async with client_context(session) as c:
            with patch('api.endpoints.auth.send_email.delay') as mock_delay:
                response = await c.post(
                    f'{settings.API_PREFIX}/auth/create_account',
                    json={
                        'name': name,
                        'email': email,
                        'password': '#Apipadoxandaonaosobemais1'
                    }
                )

                body = response.json()

                assert response.status_code == status.HTTP_201_CREATED, f'Nome {name} e E-mail {email} não cadastrado'
                assert 'id' in body
                assert isinstance(body['id'], int)
                assert body['name'] == name
                assert body['email'] == email
                mock_delay.assert_called_with(name, email)


@hypothesis_settings(deadline=None, max_examples=20)
@pytest.mark.integration
@given(
    email=st.one_of(
        st.text(min_size=1).filter(lambda x: '@' not in x),

        # 2. Ausência de domínio (ex: user@)
        st.text(min_size=1, alphabet=st.characters(
            whitelist_categories=('L', 'N')))
        .map(lambda x: f"{x}@"),

        # 3. Ausência de usuário (ex: @domain.com)
        st.text(min_size=1, alphabet=st.characters(
            whitelist_categories=('L', 'N')))
        .map(lambda x: f"@{x}.com"),

        # 4. Múltiplos símbolos '@' (ex: user@@domain.com)
        st.tuples(st.text(min_size=1), st.text(min_size=1))
        .map(lambda x: f"{x[0]}@@{x[1]}.com"),

        # 5. Caracteres proibidos no domínio (ex: user@dom!ain.com)
        st.just("user@dom!ain.com"),

        # 6. Domínio sem ponto (ex: user@domain)
        st.text(min_size=1).map(lambda x: f"{x}@domain"),

        # 7. Espaços em branco (ex: user @domain.com)
        st.text(min_size=1).map(lambda x: f"{x} @example.com")
    )
)
async def test_create_account_invalid_email(email):
    async with db_session_context() as session:
        async with client_context(session) as c:
            response = await c.post(
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
async def test_create_account_duplicate_email(client: AsyncClient, db_session):
    with patch('api.endpoints.auth.send_email.delay'):
        email: str = 'joao_duplicate@genericemail.com'

        async with db_session:
            user = (
                await UserBuilder(db_session)
                .set_email(email=email)
                .build()
            )

        assert user.active is True

        response = await client.post(
            f'{settings.API_PREFIX}/auth/create_account',
            json={
                'name': 'Felipe',
                'email': email,
                'password': '#Apipadoxandaonaosobemais1'
            }
        )
    body = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT, f'E-mail cadastrado era {user.email}'
    assert 'detail' in body
    assert isinstance(body['detail'], str) is True


@pytest.mark.integration_login
@pytest.mark.parametrize(
    'email, password',
    [
        ('felipe@teste.com', '#Apipadoxandaonaosobemais1')
    ]
)
async def test_login_success(client: AsyncClient, db_session, email, password):
    from pwdlib import PasswordHash
    password_hash: PasswordHash = PasswordHash.recommended()
    hashed_password = password_hash.hash(password)

    async with db_session:
        user = (
            await UserBuilder(db_session)
            .set_email(email)
            .set_password(hashed_password)
            .build()
        )

    data = {
        'username': email,
        'password': password
    }
    response = await client.post(
        f'{settings.API_PREFIX}/auth/login',
        data=data
    )

    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'token_type' in body
    assert body['token_type'] == 'bearer'
    assert 'access_token' in body
    assert isinstance(body['access_token'], str)
    assert body['access_token']
    assert 'refresh_token' in body
    assert isinstance(body['refresh_token'], str)
    assert body['refresh_token']
