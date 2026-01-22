from core.authentication import create_token, verify_token
from fastapi import HTTPException, status
from core.settings import settings as stt
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest
import jwt


@pytest.mark.parametrize(
    'sub, email',
    [
        ('2', 'joao@genericemail.com'),
        ('1', 'felipe@teste.com'),
        ('321', 'maria@email.com')
    ]
)
@pytest.mark.unit_create_token
def test_create_token_success(sub, email):
    payload_data = {
        "sub": sub,
        "email": email,
        "iat": int(datetime.now(tz=ZoneInfo("America/Sao_Paulo")).timestamp())
    }

    token_expires = timedelta(minutes=5)
    token = create_token(data=payload_data, expires_delta=token_expires)

    assert isinstance(token, str) is True
    decoded = jwt.decode(token, stt.SECRET_KEY, stt.ALGORITHM)
    assert decoded['sub'] == sub, 'O ID do usuário deve ser igual'
    assert decoded['email'] == email, 'O e-mail do usuário deve ser igual'
    assert 'exp' in decoded


@pytest.mark.unit_invalid_secret
def test_token_invalid_secret():
    payload_data = {
        "sub": '2',
        "email": 'felipe@teste.com',
        "iat": int(datetime.now(tz=ZoneInfo("America/Sao_Paulo")).timestamp())
    }

    token_expires = timedelta(minutes=5)
    token = create_token(data=payload_data, expires_delta=token_expires)

    with patch('core.authentication.stt.SECRET_KEY', 'wrong_secret'), pytest.raises(HTTPException) as error:
        verify_token(token)

    assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'inválido' in error.value.detail
