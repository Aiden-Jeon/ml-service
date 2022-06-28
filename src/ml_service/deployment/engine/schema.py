from typing import List
from pydantic import BaseModel, Field


class ModelInputSchema(BaseModel):

    feature_0: List[float]
    feature_1: List[float]
    feature_2: List[float]
    feature_3: List[float]
