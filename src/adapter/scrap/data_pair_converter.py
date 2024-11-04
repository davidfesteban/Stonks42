import math
from typing import List

from src.dto.data_pair import DataPair
from src.dto.time_point import TimePoint


class DataPairConverter:
    # TODO: Add Remaining Days as enricher here
    """
    @staticmethod
    def convert_to_data_pair(time_point_list: List[TimePoint]) -> List[DataPair]:
        data_pairs = []

        time_point_list = sorted(time_point_list, key=lambda tp: tp.current_etf.date)

        for i in range(len(time_point_list)):
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
    """

    @staticmethod
    def convert_to_data_pair(time_point_list: List[TimePoint], days_ahead: List[int] = [1, 3, 7, 14, 30]) -> List[
        DataPair]:
        data_pairs = []

        # Sort the list by date
        time_point_list = sorted(time_point_list, key=lambda tp: tp.current_etf.date)

        for i in range(len(time_point_list)):
            current_time_point = time_point_list[i]

            # Calculate future close prices for each day in `days_ahead`
            future_close_prices = []
            for day in days_ahead:
                if i + day < len(time_point_list):
                    future_close_price = time_point_list[i + day].current_etf.etf_close
                else:
                    future_close_price = math.nan
                future_close_prices.append(future_close_price)

            # Collect input features from the current_time_point
            inputs = []
            for field in current_time_point.__annotations__:
                market_data = getattr(current_time_point, field)
                inputs.extend([getattr(market_data, attr) for attr in market_data.__fields__])

            # Normalize future close prices by current close price
            current_close = current_time_point.current_etf.etf_close

            if current_close == 0:
                print("DEBUG: Close is 0!")

            normalized_future_close = [
                price / current_close if not math.isnan(price) and not math.isnan(current_close) else math.nan for price
                in future_close_prices]

            data_pair = DataPair(createdAt=current_time_point.current_etf.date, inputs=inputs,
                                 expected=normalized_future_close)
            data_pairs.append(data_pair)

        # Validation step to ensure consistency in input and expected sizes
        if data_pairs:
            expected_inputs_size = len(data_pairs[0].inputs)
            expected_expected_size = len(data_pairs[0].expected)

            for dp in data_pairs:
                if len(dp.inputs) != expected_inputs_size or len(dp.expected) != expected_expected_size:
                    raise ValueError("Inconsistent sizes in DataPair: "
                                     f"inputs={len(dp.inputs)}, expected={len(dp.expected)}, "
                                     f"expected sizes: inputs={expected_inputs_size}, expected={expected_expected_size}")

        return data_pairs
