from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.models.answers import AnswerORM
from src.db.models.questions import QuestionORM
from src.helpers.schemas.answers import CreateAnswer, AnswerResponse
from src.helpers.enums.question import QuestionStatus
from src.exceptions.database import NotFoundError
from src.utils.misc import MiscUtils
from src.helpers.enums.user import RoleEnum
class AnswerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_answer(self, payload: CreateAnswer, current_user) -> AnswerResponse:
        user_id = None
        if current_user and current_user.get("role") == RoleEnum.ADMIN.value:
            user_id = current_user.get("user_id")

        # Check if the question exists
        stmt = select(QuestionORM).filter_by(id=payload.question_id)
        result = await self.session.execute(stmt)
        question = result.scalar_one_or_none()

        if not question:
            raise NotFoundError("Question not found")

        # Create the answer
        answer = AnswerORM(
            id=MiscUtils.generate_uuid(),
            user_id=user_id,
            question_id=payload.question_id,
            message=payload.message,
        )

        self.session.add(answer)
        await self.session.commit()
        await self.session.refresh(answer)

        return AnswerResponse.model_validate(answer)