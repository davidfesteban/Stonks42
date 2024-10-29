from typing import List

from src.dto.data_pair import DataPair
from src.dto.time_point import TimePoint


class DataPairConverter:
    @staticmethod
    def convert_to_data_pair(time_point_list: List[TimePoint]) -> List[DataPair]:
        data_pairs = []
        timepoints = sorted(time_point_list, key=lambda tp: tp.current_etf.date)

        for idx, time_point in enumerate(timepoints):
            base_date = time_point.current_etf.date
            if not all(getattr(time_point, field).date == base_date for field in time_point.__annotations__):
                raise ValueError("Inconsistent dates found in TimePoint")

            inputs = []
            for field in time_point.__annotations__:
                market_data = getattr(time_point, field)
                if market_data is not None:
                    inputs.extend([
                        float(getattr(market_data, attr)) if getattr(market_data, attr) is not None else 0.0
                        for attr in market_data.__fields__
                    ])


            if idx + 1 < len(timepoints):
                tomorrow_close = timepoints[idx + 1].current_etf.etf_close
                if tomorrow_close < time_point.current_etf.etf_close:
                    expected = 0
                elif tomorrow_close == time_point.current_etf.etf_close:
                    expected = 1
                else:
                    expected = 2
            else:
                print("No data for tomorrow!. Today: " + time_point.current_etf.date)
                expected = None

            created_at = base_date

            if expected is not None:
                data_pair = DataPair(
                    createdAt=created_at,
                    inputs=inputs,
                    expected=expected
                )
                data_pairs.append(data_pair)

        return data_pairs

