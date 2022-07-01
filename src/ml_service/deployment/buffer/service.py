from datetime import datetime
import pandas as pd

from ml_service.deployment.buffer.schema import InferenceIn
from ml_service.deployment.buffer.repository import BufferRepository
from ml_service.deployment.engine.service import MODEL_ENGINE



class BufferService:
    def __init__(self) -> None:
        self._buffer_repo = BufferRepository()

    def infer_schema(self, inputs: InferenceIn) -> pd.DataFrame:
        raw = {key: [value] for key, value in inputs.dict().items()}
        df = pd.DataFrame.from_dict(raw, orient="columns")
        return df

    def inference(self, predict_method: str, inputs: InferenceIn):
        timestamp = datetime.utcnow()
        df = self.infer_schema(inputs)
        self._buffer_repo.add_input(timestamp=timestamp, **inputs.dict())

        result = MODEL_ENGINE.inference(df=df, predict_method=predict_method)
        result_df = pd.DataFrame(result)
        return result_df
