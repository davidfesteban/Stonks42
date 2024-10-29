from typing import List

from pydantic import BaseModel


class DataPair(BaseModel):
    createdAt: int  # ID
    inputs: List[float]
    expected: List[float]

    class Config:
        populate_by_name = True  # Allows using field names directly
        extra = "ignore"  # Ignores fields not defined in the model, like `_id`
