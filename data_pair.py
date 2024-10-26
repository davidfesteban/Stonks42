from dataclasses import dataclass
from typing import List


@dataclass
class DataPair:
    uuid: str
    topic: str
    createdAt: int
    inputs: List[float]
    expected: List[float]
