from pydantic import BaseModel, Field
from typing import Optional
from src.helpers.enums.question import QuestionStatus
from datetime import datetime

class CreateQuestion(BaseModel):
    message: str = Field(..., max_length=200)


class QuestionResponse(BaseModel):
    id: str
    user_id: Optional[str]
    message: str
    status: QuestionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes  = True
