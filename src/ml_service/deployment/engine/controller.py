from fastapi import APIRouter

from ml_service.deployment.engine.schema import InferenceIn
from ml_service.deployment.engine.service import engine

router = APIRouter(prefix="/engine")


@router.post("/{predict_method}")
def inference(predict_method: str, inputs: InferenceIn):
    result = engine.inference(predict_method, inputs)
    return result
