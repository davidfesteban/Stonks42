from typing import List

from pydantic import BaseModel


class DataPair(BaseModel):
    _id: int  # Define `_id` directly as the primary key
    inputs: List[float]
    expected: List[float]

    # Optional property to access `_id` as `createdAt` if needed
    @property
    def createdAt(self):
        return self._id

    class Config:
        extra = "ignore"  # Ignore fields not defined in the model
