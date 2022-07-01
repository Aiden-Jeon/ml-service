from typing import List
from pydantic import BaseModel


class InferenceIn(BaseModel):

    feature_0: float
    feature_1: float
    feature_2: float
    feature_3: float
