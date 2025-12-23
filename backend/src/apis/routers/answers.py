from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.services.answers import AnswerService
from src.helpers.schemas.api_response import APIResponse
from src.helpers.schemas.answers import CreateAnswer
from src.apis.security import get_optional_current_user
router = APIRouter(
    prefix="/answers",
    tags=["answers"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_answer(request: Request,
    payload: CreateAnswer,
    session: AsyncSession = Depends(get_async_session),

):
    current_user: dict | None = None
    token = request.headers.get("Authorization")
    if token:
        current_user = await get_optional_current_user(token.split(" ")[1])

    service = AnswerService(session)

    answer = await service.create_answer(payload, current_user)

    return APIResponse(
        status=status.HTTP_201_CREATED,
        message="Answer posted successfully",
        data=answer.model_dump(),
    )