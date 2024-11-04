from collections import defaultdict
from typing import Dict, List

from src.dto.market_data import MarketData
from src.dto.time_point import TimePoint


class TimePointConverter:

    @staticmethod
    def group_and_convert(data: Dict[str, List[MarketData]]) -> List[TimePoint]:
        grouped_data = defaultdict(lambda: {field: None for field in TimePoint.__annotations__.keys()})

        for field_name, market_data_list in data.items():
            for market_data in market_data_list:
                grouped_data[market_data.date][field_name] = market_data

        time_points = []
        for date, fields in grouped_data.items():
            fields = {key: value for key, value in fields.items() if key in TimePoint.__annotations__}
            time_point = TimePoint(**fields)
            time_points.append(time_point)

        return time_points
