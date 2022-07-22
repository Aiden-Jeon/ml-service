from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator


class PathSettings(BaseSettings):
    MODEL_ARTIFACT_PATH: str


class DataBaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    USE_BUFFER: bool
    POSTGRES_URL: Optional[str] = None

    @validator(
        "POSTGRES_URL",
        pre=True,
    )
    def _generate_postgres_url(
        cls,
        v: Optional[str],
        values: Dict[str, Any],
        field: str,
    ) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


class Settings(
    PathSettings,
    DataBaseSettings,
):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


load_dotenv(Path(__file__).parent / "common.env")
settings = Settings()

print(settings)
