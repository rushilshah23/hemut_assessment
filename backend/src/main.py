from fastapi import FastAPI
from src.config import Config

from src.exceptions.base import AppException
from src.apis.exception_handlers import (
    app_exception_handler,
    unhandled_exception_handler,
    value_exception_handler
)


def create_app(config:Config):
    app = FastAPI()
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(Exception, value_exception_handler)
    
    
    
    from src.apis.routers.users import router as users_router
    app.include_router(users_router)
    from src.apis.routers.questions import router as questions_router
    app.include_router(questions_router)
    from src.apis.routers.answers import router as answers_router
    app.include_router(answers_router)

    from src.ws.router import router as ws_router
    app.include_router(ws_router)
    
    @app.get("/health")
    async def get_health():
        return {"message":"Healthy"}
    
    return app


app = create_app(config=Config)
