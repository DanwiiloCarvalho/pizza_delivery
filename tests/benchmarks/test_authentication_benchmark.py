from core.authentication import create_token, verify_token
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def test_create_token_benchmark(benchmark):
    payload_data = {
        "sub": '2',
        "email": 'joao@genericemail.com',
        "iat": int(datetime.now(tz=ZoneInfo("America/Sao_Paulo")).timestamp())
    }
    token_expires = timedelta(minutes=5)
    result: str = benchmark.pedantic(
        create_token, args=(payload_data, token_expires), iterations=10, rounds=100)
    assert isinstance(result, str) is True


def test_verify_token_benchmark(benchmark):
    payload_data = {
        "sub": '2',
        "email": 'joao@genericemail.com',
        "iat": int(datetime.now(tz=ZoneInfo("America/Sao_Paulo")).timestamp())
    }
    token_expires = timedelta(minutes=5)
    token: str = create_token(payload_data, token_expires)
    result = benchmark(verify_token, token)
