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
            next_day_time_point = time_point_list[i + 1].current_etf.etf_close
            next_three_days_time_point = time_point_list[i + 3].current_etf.etf_close if len(
                time_point_list) - 1 > i + 3 else 0.0
            next_week_time_point = time_point_list[i + 7].current_etf.etf_close if len(
                time_point_list) - 1 > i + 7 else 0.0

            inputs = []
            for field in current_time_point.__annotations__:
                market_data = getattr(current_time_point, field)
                # Add all values of MarketData to inputs, including 'date' and 'day_of_week'
                inputs.extend([
                    getattr(market_data, attr) if getattr(market_data, attr) is not None else 0.0
                    for attr in market_data.__fields__
                ])

            current_close = current_time_point.current_etf.etf_close
            current_close = current_close if current_close > 0 else 1

            data_pair = DataPair(
                createdAt=current_time_point.current_etf.date,
                inputs=inputs,
                expected=[next_day_time_point / current_close, next_three_days_time_point / current_close,
                          next_week_time_point / current_close]
            )
            data_pairs.append(data_pair)

        return data_pairs
