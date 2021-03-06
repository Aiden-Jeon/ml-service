from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session

from ml_service.deployment.buffer.model import *
from ml_service.deployment.settings import settings
from ml_service.deployment.store.base import Base


class Database:
    def __init__(
        self,
        db_url: str = str(settings.POSTGRES_URL),
    ) -> None:
        if settings.USE_BUFFER:
            self.engine = create_engine(db_url)
            self._session = orm.scoped_session(
                orm.sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine,
                ),
            )

    def create_database(self):
        print("create database")
        Base.metadata.create_all(self.engine)
        print("created database")

    @property
    def session(self) -> Session:
        return self._session
