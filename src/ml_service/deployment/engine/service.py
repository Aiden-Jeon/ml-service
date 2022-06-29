import os
from pathlib import Path

import cloudpickle
import pandas as pd

from ml_service.deployment.engine.schema import InferenceIn
from ml_service.deployment.settings import settings

MODEL_ARTIFACT_PATH = os.getenv("MODEL_ARTIFACT_PATH")


class EngineService:
    def __init__(self) -> None:
        self.artifact_path = Path(settings.MODEL_ARTIFACT_PATH)
        self._model = ...
        self._load_model()

    def _load_model(self) -> None:
        with open(self.artifact_path / "model.pkl", "rb") as f:
            self._model = cloudpickle.load(f)

    def infer_schema(self, inputs: InferenceIn) -> pd.DataFrame:
        raw = {key: value for key, value in inputs.dict().items()}
        df = pd.DataFrame.from_dict(raw, orient="columns")
        return df

    def inference(self, predict_method: str, inputs: InferenceIn):
        df = self.infer_schema(inputs)
        result = getattr(self._model, predict_method)(df)
        result_df = pd.DataFrame(result)
        return result_df


engine = EngineService()
