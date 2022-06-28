from fastapi import APIRouter

from .schema import ModelInputSchema
from .service import ModelService

router = APIRouter()

model = ModelService("./", "model")


@router.post("/inference/{predict_method}")
def inference(predict_method: str, inputs: ModelInputSchema):
    result = model.inference(predict_method, inputs)
    return result
