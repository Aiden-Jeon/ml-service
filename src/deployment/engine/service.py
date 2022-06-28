from pathlib import Path

import cloudpickle
import pandas as pd

from .schema import ModelInputSchema


class ModelService:
    def __init__(self, artifact_path: str, model_name: str) -> None:
        self.artifact_path = Path(artifact_path) / model_name
        self._model = ...
        self._load_model()

    def _load_model(self) -> None:
        with open(self.artifact_path / "model.pkl", "rb") as f:
            self._model = cloudpickle.load(f)

    def infer_schema(self, inputs: ModelInputSchema) -> pd.DataFrame:
        raw = {key: value for key, value in inputs.dict().items()}
        df = pd.DataFrame.from_dict(raw, orient="columns")
        return df

    def inference(self, predict_method: str, inputs: ModelInputSchema):
        df = self.infer_schema(inputs)
        result = getattr(self._model, predict_method)(df)
        result_df = pd.DataFrame(result)
        return result_df
