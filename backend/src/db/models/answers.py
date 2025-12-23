from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func
from .timestampmixin import TimestampMixin

class AnswerORM(Base, TimestampMixin):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=False,
        nullable=True
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("questions.id"),
        unique=False,
        nullable=False
    )
    message: Mapped[str] = mapped_column(
        String(200),
        unique=False,
        nullable=False
    )

