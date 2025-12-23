from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import String, ForeignKey, DateTime, func, Enum as SAEnum, text
from src.helpers.enums.question import QuestionStatus
from .timestampmixin import TimestampMixin


class QuestionORM(Base, TimestampMixin):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=False,
        nullable=True
    )
    message: Mapped[str] = mapped_column(
        String(200),
        unique=False,
        nullable=False
    )
    # status: Mapped[QuestionStatus] = mapped_column(
    #     SAEnum(
    #         QuestionStatus,
    #         name="question_status_enum",
    #         create_constraint=True
    #     ),
    #     nullable=False,
    #     server_default=text("'pending'::question_status_enum")
    # )
    
    status = sa.Column(
    'status',
    sa.Enum('pending', 'answered', 'escalated', name='question_status_enum'),
    server_default=text("'pending'::question_status_enum"),
    nullable=False
)