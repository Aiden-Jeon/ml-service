from fastapi import FastAPI

from ml_service.deployment.engine.controller import router as engine_router
from ml_service.deployment.buffer.controller import router as buffer_router
from ml_service.deployment.store.db import Database


def creat_app():
    app_ = FastAPI()

    db = Database()

    app_.include_router(engine_router)
    app_.include_router(buffer_router)
    return app_


app = creat_app()
