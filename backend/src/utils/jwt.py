# src/utils/jwt.py
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

import jwt

from src.config import Config
from src.exceptions.auth import InvalidTokenError


class JWTUtils:

    @staticmethod
    def generate_access_token(
        subject: str,
        payload: Dict[str, Any] | None = None,
        expires_in_minutes: int | None = None,
    ) -> str:
        """
        subject → usually user_id
        payload → role, email, etc
        """

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=expires_in_minutes or Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

        token_payload = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }

        if payload:
            token_payload.update(payload)

        return jwt.encode(
            token_payload,
            Config.JWT_SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM,
        )

    @staticmethod
    def verify_access_token(token: str) -> Dict[str, Any]:
        try:
            decoded = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM],
            )
            return decoded

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token expired")

        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")
