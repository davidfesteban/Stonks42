from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

class DataPair(BaseModel):
    uuid: UUID = Field(alias="_id")
    createdAt: int
    inputs: List[float]
    expected: List[float]

    class Config:
        populate_by_name = True  # Allows using field names directly
        extra = "ignore"  # Ignores fields not defined in the model, like `_id`
