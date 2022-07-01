from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd

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
        timestamp: Optional[datetime],
        **kwargs,
    ) -> DataIn:
        if not self.ready:
            raise NotImplementedError("db is not ready")

        data_in = DataIn(
            timestamp=timestamp,
            **kwargs,
        )

        with self.session() as s:
            s.add(data_in)
            s.commit()
            s.refresh(data_in)

        return data_in
