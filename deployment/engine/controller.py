from fastapi import APIRouter

from .schema import ModelInputSchema
from .service import ModelEngine

router = APIRouter()

engine = ModelEngine("./", "model")
engine.load()


@router.post("/predict")
def predict(inputs: ModelInputSchema):
    inputs
    return engine.model.predict(inputs)
