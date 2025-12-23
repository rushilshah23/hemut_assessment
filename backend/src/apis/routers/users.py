from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.services.users import UserService
from src.helpers.enums.user import RoleEnum
from src.helpers.schemas.users import CreateAdmin
from src.helpers.schemas.api_response import APIResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

from src.exceptions.database import DuplicateResourceError

@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def create_admin_user(
    create_admin_schema: CreateAdmin,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session)

    # try:
    create_admin_response = await service.create_admin_user(create_admin_schema)

    return APIResponse(
        status=status.HTTP_201_CREATED,
        message="Admin created successfully",
        data=create_admin_response.model_dump(),
    )

    # except DuplicateResourceError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=str(e),
    #     )

    # except ValueError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=str(e),
    #     )