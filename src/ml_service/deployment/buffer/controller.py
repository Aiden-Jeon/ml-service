from fastapi import APIRouter, Depends

from ml_service.deployment.buffer.schema import InferenceIn
from ml_service.deployment.buffer.service import BufferService

router = APIRouter(prefix="/buffer")


@router.post("/{predict_method}")
def inference(
    predict_method: str,
    inputs: InferenceIn,
    buffer_service: BufferService = Depends(BufferService),
):
    result = buffer_service.inference(predict_method, inputs)
    return result
