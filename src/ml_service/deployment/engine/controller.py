from fastapi import APIRouter, Depends

from ml_service.deployment.engine.schema import InferenceIn
from ml_service.deployment.engine.service import MODEL_ENGINE

router = APIRouter(prefix="/engine")


@router.post("/{predict_method}")
def inference(predict_method: str, inputs: InferenceIn):
    df = MODEL_ENGINE.infer_schema(inputs=inputs)
    result = MODEL_ENGINE.inference(df=df, predict_method=predict_method)
    return result
