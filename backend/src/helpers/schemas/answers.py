from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateAnswer(BaseModel):
    question_id: str = Field(..., description="ID of the question being answered")
    message: str = Field(..., max_length=200, description="Answer message")

class AnswerResponse(BaseModel):
    id: str
    question_id: str
    user_id: Optional[str]
    message: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True