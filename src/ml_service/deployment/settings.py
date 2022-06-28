from pydantic import BaseSettings


class PathEnvironment(BaseSettings):
    MODEL_ARTIFACT_PATH: str


settings = PathEnvironment()
