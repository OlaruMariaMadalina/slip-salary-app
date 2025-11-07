import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings


def create_access_token(*, user_id: int, expires: timedelta | None = None) -> str:
    """
    Generate a JWT access token for a given user ID.

    Args:
        user_id (int): The ID of the user for whom the token is generated.
        expires (timedelta | None): Optional expiration time for the token. Defaults to settings.JWT_EXPIRE_MINUTES.

    Returns:
        str: Encoded JWT token as a string.
    """
    exp_delta = expires or timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + exp_delta).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token and extract the user ID.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: Dictionary containing the user_id if decoding is successful.

    Raises:
        Exception: If the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return {
            "user_id": payload.get("user_id"),
        }
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")