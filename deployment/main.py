from fastapi import FastAPI

from engine.controller import router as engine_router


def creat_app():
    app_ = FastAPI()

    app_.include_router(engine_router)
    return app_


app = creat_app()
