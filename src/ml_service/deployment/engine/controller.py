from fastapi import APIRouter

from ml_service.deployment.engine.schema import InferenceIn
from ml_service.deployment.engine.service import ModelService

router = APIRouter(prefix="/engine")

model = ModelService()


@router.post("/inference/{predict_method}")
def inference(predict_method: str, inputs: InferenceIn):
    result = model.inference(predict_method, inputs)
    return result
