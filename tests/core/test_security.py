from core.security import generate_hash, verify_password, password_hash
from unittest.mock import patch
import pytest


@pytest.mark.unit_generate_hash
def test_generate_hash_returns_valid_hash():
    generated_hash: str = generate_hash('#Apipadoxandaonaosobemais1')

    assert isinstance(generated_hash, str)
    assert password_hash.verify(
        password='#Apipadoxandaonaosobemais1', hash=generated_hash)


@pytest.mark.unit_generate_hash
def test_generate_hash_is_not_deterministic():
    generated_hash1: str = generate_hash('#Apipadoxandaonaosobemais1')
    generated_hash2: str = generate_hash('#Apipadoxandaonaosobemais1')

    assert generated_hash1 != generated_hash2


@pytest.mark.unit_generate_hash
def test_generate_hash_calls_pwdlib():
    with patch('core.security.password_hash') as mock_password_hash:
        mock_password_hash.hash.return_value = 'fake_hash'

        result: str = generate_hash('senha')
        mock_password_hash.hash.assert_called_once_with('senha')
        assert result == 'fake_hash'


@pytest.mark.unit_verify_password
def test_verify_password_success():
    password: str = '#Apipadoxandaonaosobemais1'
    hashed_password: str = generate_hash(password)

    assert verify_password(password, hashed_password) is True


@pytest.mark.unit_verify_password
def test_verify_password_failure():
    password: str = '#Apipadoxandaonaosobemais1'
    wrong_password: str = 'wrong_password'

    hashed_password: str = generate_hash(password)

    assert verify_password(wrong_password, hashed_password) is False
