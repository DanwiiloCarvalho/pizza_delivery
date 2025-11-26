from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from core.settings import settings as stt
import jwt


def create_access_token(data: dict[str, any], expires_delta: timedelta | None = None) -> str:
    data_to_encode = data.copy()
    now: datetime = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)

    data_to_encode.update({"exp": expire})
    enconded_jwt: str = jwt.encode(payload=data_to_encode,
                                   key=stt.SECRET_KEY, algorithm=stt.ALGORITHM)

    return enconded_jwt
