from datetime import datetime
from typing import Any, Dict, Optional

from ml_service.deployment.store import Database
from ml_service.deployment.buffer.model import DataIn


class BufferRepository:
    def __init__(
        self,
    ) -> None:
        db = Database()
        self.session = db.session
        self.ready = db.ready

    def add_input(
        self,
        inputs: Dict[str, Any],
        timestamp: Optional[datetime],
    ) -> DataIn:
        if not self.ready:
            raise NotImplementedError("db is not ready")

        inputs = DataIn(
            **inputs,
            timestamp,
        )

        with self.session() as s:
            s.add(inputs)
            s.commit()
            s.refresh(inputs)

        return inputs
