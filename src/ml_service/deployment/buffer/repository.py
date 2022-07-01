from datetime import datetime

from ml_service.deployment.settings import settings
from ml_service.deployment.store import Database
from ml_service.deployment.buffer.model import DataIn
from ml_service.deployment.response_fail import BadRequest


class BufferRepository:
    def __init__(
        self,
    ) -> None:
        db = Database()

    def add_input(
        self,
        timestamp: datetime,
        **kwargs,
    ) -> DataIn:
        data_in = DataIn(
            timestamp=timestamp,
            **kwargs,
        )
        if not settings.USE_BUFFER:
            raise BadRequest("USE_BUFFER is False")

        with self.db.session() as s:
            s.add(data_in)
            s.commit()
            s.refresh(data_in)

        return data_in
