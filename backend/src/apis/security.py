from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.jwt import JWTUtils

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    payload = JWTUtils.verify_access_token(token)
    return payload

from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.services.users import UserService
from src.exceptions.auth import InvalidTokenError
from src.apis.security import get_current_user

async def get_optional_current_user(
    token:str):
    try:
        payload = await JWTUtils.verify_optional_access_token(token)
        return payload
    except InvalidTokenError:
        return None   