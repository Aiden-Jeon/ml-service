from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from ml_service.deployment.settings import settings


class Database:
    def __init__(
        self,
        db_url: str = str(settings.POSTGRES_URL),
    ) -> None:
        self.engine = create_engine(db_url)
        try:
            self.engine.connect()
            self._ready = True
        except OperationalError:
            self._ready = False
        self._session = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                binds=self.engine,
            ),
        )

    @property
    def session(self) -> Session:
        return self._session

    @property
    def ready(self) -> bool:
        return self._ready
