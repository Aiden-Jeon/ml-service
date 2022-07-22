from fastapi import FastAPI

from ml_service.deployment.buffer.controller import router as buffer_router
from ml_service.deployment.engine.controller import router as engine_router
from ml_service.deployment.settings import settings
from ml_service.deployment.store.db import Database


def creat_app():
    app_ = FastAPI()
    if settings.USE_BUFFER:
        db = Database()
        db.create_database()

    app_.include_router(engine_router)
    app_.include_router(buffer_router)
    return app_


app = creat_app()
