from typing import List

from src.dto.data_pair import DataPair
from src.dto.time_point import TimePoint


class DataPairConverter:
    @staticmethod
    def convert_to_data_pair(time_point_list: List[TimePoint]) -> List[DataPair]:
        data_pairs = []

        time_point_list = sorted(time_point_list, key=lambda tp: tp.current_etf.date if tp.current_etf else 0)

        for i in range(len(time_point_list) - 1):
            current_time_point = time_point_list[i]
            next_time_point = time_point_list[i + 1]

            inputs = []
            for field in current_time_point.__annotations__:
                market_data = getattr(current_time_point, field)
                # Add all values of MarketData to inputs, including 'date' and 'day_of_week'
                inputs.extend([
                    getattr(market_data, attr) if getattr(market_data, attr) is not None else 0.0
                    for attr in market_data.__fields__
                ])

            current_close = current_time_point.current_etf.etf_close
            next_close = next_time_point.current_etf.etf_close
            if next_close < current_close:
                expected = 0
            elif next_close == current_close:
                expected = 1
            else:
                expected = 2

            data_pair = DataPair(
                createdAt=current_time_point.current_etf.date,
                inputs=inputs,
                expected=[expected]
            )
            data_pairs.append(data_pair)

        return data_pairs
