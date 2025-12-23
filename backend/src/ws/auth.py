import jwt
from src.config import Config
from src.exceptions.auth import InvalidTokenError

def decode_ws_token(token: str | None):
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return payload
    except jwt.PyJWTError:
        raise InvalidTokenError("Invalid WS token")
