import uuid
from datetime import datetime
from sqlalchemy import select, case, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.questions import QuestionORM
from src.helpers.enums.question import QuestionStatus
from src.helpers.enums.user import RoleEnum
from src.helpers.schemas.questions import CreateQuestion, QuestionResponse


class QuestionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_question(
        self,
        payload: CreateQuestion,
        current_user: dict | None = None,
    ) -> QuestionResponse:

        user_id = None
        if current_user and current_user.get("role") == RoleEnum.ADMIN.value:
            user_id = current_user.get("user_id")

        question = QuestionORM(
            id=str(uuid.uuid4()),
            user_id=user_id,
            message=payload.message,
            status=QuestionStatus.PENDING,
        )

        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)

        return QuestionResponse.model_validate(question)

    async def get_all_questions(self) -> list[QuestionResponse]:
        stmt = (
            select(QuestionORM)
            .order_by(
                case(
                    (QuestionORM.status == QuestionStatus.ESCALATED, 0),
                    else_=1,
                ),
                desc(QuestionORM.updated_at),
            )
        )

        result = await self.session.execute(stmt)
        questions = result.scalars().all()
        return [QuestionResponse.model_validate(q) for q in questions]

    async def mark_as_answered(self, question_id: str) -> QuestionResponse:
        question = await self._get_question_or_404(question_id)

        question.status = QuestionStatus.ANSWERED
        question.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(question)

        return QuestionResponse.model_validate(question)

    async def mark_as_escalated(self, question_id: str) -> QuestionResponse:
        question = await self._get_question_or_404(question_id)

        question.status = QuestionStatus.ESCALATED
        question.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(question)

        return QuestionResponse.model_validate(question)

    async def _get_question_or_404(self, question_id: str) -> QuestionORM:
        stmt = select(QuestionORM).where(QuestionORM.id == question_id)
        result = await self.session.execute(stmt)
        question = result.scalar_one_or_none()

        if not question:
            raise ValueError("Question not found")

        return question
