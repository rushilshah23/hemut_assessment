from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.services.questions import QuestionService
from src.helpers.schemas.questions import CreateQuestion
from src.helpers.schemas.api_response import APIResponse
from src.apis.security import get_current_user, get_optional_current_user
from src.exceptions.auth import InvalidTokenError

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_question(
    request: Request,
    payload: CreateQuestion,
    session: AsyncSession = Depends(get_async_session),

):
    current_user: dict | None = None
    token = request.headers.get("Authorization")
    if token:
        try:
            current_user = await get_optional_current_user(token.split(" ")[1])
        except InvalidTokenError:
            current_user = None
    service = QuestionService(session)

    question = await service.create_question(payload, current_user)

    return APIResponse(
        status=status.HTTP_201_CREATED,
        message="Question created successfully",
        data=question.model_dump(),
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_questions(
    session: AsyncSession = Depends(get_async_session),
):
    service = QuestionService(session)

    questions = await service.get_all_questions()

    return APIResponse(
        status=status.HTTP_200_OK,
        message="Questions fetched successfully",
        data=[q.model_dump() for q in questions],
    )


@router.put("/{question_id}/answer", status_code=status.HTTP_200_OK)
async def mark_question_as_answered(
    request:Request,
    question_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
):

    service = QuestionService(session)

    question = await service.mark_question_as_answered(question_id)

    return APIResponse(
        status=status.HTTP_200_OK,
        message="Question marked as answered successfully",
        data=question.model_dump(),
    )


@router.put("/{question_id}/escalate", status_code=status.HTTP_200_OK)
async def mark_question_as_answered(
    request:Request,
    question_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
):

    service = QuestionService(session)

    question = await service.mark_question_as_escalate(question_id)

    return APIResponse(
        status=status.HTTP_200_OK,
        message="Question escalated successfully",
        data=question.model_dump(),
    )
