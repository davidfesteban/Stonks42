import math
from statistics import mean, stdev
from typing import Dict, List, Optional

from src.dto.market_data import MarketData



class MovingAverageCalculator:

    @staticmethod
    def calculate_moving_average(values: List[float], window: int) -> Optional[float]:
        # Filter out NaN values, keeping valid ones in the calculation
        valid_values = [v for v in values[-window:] if not math.isnan(v)]
        return mean(valid_values) if valid_values else math.nan  # Only calculate if we have valid values

    @staticmethod
    def calculate_rolling_std(values: List[float], window: int) -> Optional[float]:
        # Filter out NaN values
        valid_values = [v for v in values[-window:] if not math.isnan(v)]
        return stdev(valid_values) if len(valid_values) > 1 else math.nan  # stdev requires at least 2 values

    @staticmethod
    def calculate_high_low(values: List[float], window: int, high: bool = True) -> Optional[float]:
        # Filter out NaN values
        valid_values = [v for v in values[-window:] if not math.isnan(v)]
        if not valid_values:
            return math.nan
        return max(valid_values) if high else min(valid_values)

    @staticmethod
    def fill_moving_averages(market_data_list: Dict[str, List['MarketData']]) -> Dict[str, List['MarketData']]:
        for etf, data_list in market_data_list.items():
            data_list.sort(key=lambda data: data.date)

            # Lists to hold past values for rolling calculations
            volume_values = []
            close_values = []
            high_values = []
            low_values = []

            for data in data_list:
                # Append all values to rolling lists, including NaN
                volume_values.append(data.etf_volume)
                close_values.append(data.etf_close)
                high_values.append(data.etf_high)
                low_values.append(data.etf_low)

                # Calculate and set moving averages for volume
                data.average_5_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 5)
                data.average_10_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 10)
                data.average_20_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 20)
                data.average_30_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 30)
                data.average_50_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 50)
                data.average_100_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 100)
                data.average_200_days_volume = MovingAverageCalculator.calculate_moving_average(volume_values, 200)

                # Calculate and set moving averages for close prices
                data.average_5_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 5)
                data.average_10_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 10)
                data.average_20_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 20)
                data.average_30_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 30)
                data.average_50_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 50)
                data.average_100_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 100)
                data.average_200_days_close = MovingAverageCalculator.calculate_moving_average(close_values, 200)

                # Calculate and set 52-week high/low (252 trading days)
                data.etf_week_52_high = MovingAverageCalculator.calculate_high_low(high_values, 252, high=True)
                data.etf_week_52_low = MovingAverageCalculator.calculate_high_low(low_values, 252, high=False)

                # Calculate and set volatility as rolling standard deviation of close prices
                data.volatility_10_days = MovingAverageCalculator.calculate_rolling_std(close_values, 10)
                data.volatility_20_days = MovingAverageCalculator.calculate_rolling_std(close_values, 20)
                data.volatility_30_days = MovingAverageCalculator.calculate_rolling_std(close_values, 30)

        return market_data_list