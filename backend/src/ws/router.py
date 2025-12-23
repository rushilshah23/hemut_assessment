from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.ws.manager import ConnectionManager
from src.ws.auth import decode_ws_token
from src.db.session import async_session_factory
from src.services.questions import QuestionService
from src.services.answers import AnswerService
from src.helpers.enums.user import RoleEnum
from src.helpers.schemas.questions import CreateQuestion
from src.helpers.schemas.answers import CreateAnswer

router = APIRouter()
manager = ConnectionManager()

def _ensure_admin(user: dict):
    if not user or user.get("role") != RoleEnum.ADMIN.value:
        raise PermissionError("Admin only")

def is_admin(user: dict) -> bool:
    return bool(user and user.get("role") == RoleEnum.ADMIN.value)


@router.websocket("/ws/questions")
async def questions_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")

    try:
        user = decode_ws_token(token)
    except Exception:
        await websocket.close(code=1008)
        return

    # await manager.connect(websocket)
    await manager.connect(websocket, user)

    async with async_session_factory() as session:
        service = QuestionService(session)
        questions = await service.get_all_questions()
        await websocket.send_json({
            "event": "INITIAL_QUESTIONS",
            "data": [q.model_dump(mode="json") for q in questions],
        })
    try:
        while True:
            message = await websocket.receive_json()
            event = message.get("event")
            data = message.get("data")

            async with async_session_factory() as session:

                question_service = QuestionService(session)
                answer_service = AnswerService(session)
                if event == "CREATE_QUESTION":
                    data = CreateQuestion.model_validate(data)
                    question = await service.create_question(data, user)
                    # await manager.broadcast({
                    #     "event": "QUESTION_CREATED",
                    #     "data": question.model_dump(mode="json"),
                    # })
                    questions = await service.get_all_questions()
                    await websocket.send_json({
                        "event": "QUESTION_UPDATED",
                        "data": [q.model_dump(mode="json") for q in questions],
                    })
                    # await manager.broadcast({
                    #     "event": "QUESTION_UPDATED",
                    #     "data": question.model_dump(mode="json"),
                    # })
                    await manager.broadcast_to_admins({
                        "event": "ADMIN_NOTIFICATION",
                        "data": {
                            "type": "NEW_QUESTION",
                            "question_id": question.id,
                            "message": question.message,
                        }
                    })
                elif event == "ANSWER_QUESTION":
                    data = CreateAnswer.model_validate(data)
                    answer = await answer_service.create_answer(data, user)
                    # await manager.broadcast({
                    #     "event": "ANSWER_CREATED",
                    #     "data": answer.model_dump(mode="json"),
                    # })
                    questions = await service.get_all_questions()
                    await websocket.send_json({
                        "event": "QUESTION_UPDATED",
                        "data": [q.model_dump(mode="json") for q in questions],
                    })
                    # await manager.broadcast({
                    #     "event": "QUESTION_UPDATED",
                    #     "data": question.model_dump(mode="json"),
                    # })
                elif event == "MARK_QUESTION_AS_ANSWERED":
                    # _ensure_admin(user)
                    if not is_admin(user):
                        await websocket.send_json({
                            "event": "ERROR",
                            "message": "Admin only action"
                        })
                        continue
                    question = await question_service.mark_as_answered(data["question_id"])
                    # await manager.broadcast({
                    #     "event": "QUESTION_ANSWERED",
                    #     "data": question.model_dump(mode="json"),
                    # })
                    questions = await service.get_all_questions()
                    await websocket.send_json({
                        "event": "QUESTION_UPDATED",
                        "data": [q.model_dump(mode="json") for q in questions],
                    })
                    # await manager.broadcast({
                    #     "event": "QUESTION_UPDATED",
                    #     "data": question.model_dump(mode="json"),
                    # })
                elif event == "MARK_QUESTION_AS_ESCALATED":
                    # _ensure_admin(user)
                    if not is_admin(user):
                        await websocket.send_json({
                            "event": "ERROR",
                            "message": "Admin only action"
                        })
                        continue
                    question = await question_service.mark_as_escalated(data["question_id"])
                    # await manager.broadcast({
                    #     "event": "QUESTION_ESCALATED",
                    #     "data": question.model_dump(),
                    # })
                    questions = await service.get_all_questions()
                    await websocket.send_json({
                        "event": "QUESTION_UPDATED",
                        "data": [q.model_dump(mode="json") for q in questions],
                    })
                    # await manager.broadcast({
                    #     "event": "QUESTION_UPDATED",
                    #     "data": question.model_dump(mode="json"),
                    # })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
