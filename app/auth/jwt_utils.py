import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings


def create_access_token(*, user_id: int, expires: timedelta | None = None) -> str:
    exp_delta = expires or timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + exp_delta).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_jwt(token: str) -> dict:
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return {
            "user_id": payload.get("user_id"),
        }
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")