from pwdlib import PasswordHash

password_hash: PasswordHash = PasswordHash.recommended()


def generate_hash(password: str) -> str:
    hashed_password = password_hash.hash(password)

    return hashed_password
