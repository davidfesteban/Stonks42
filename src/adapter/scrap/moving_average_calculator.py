from statistics import mean, stdev
from typing import Dict, List, Optional

from src.dto.market_data import MarketData


class MovingAverageCalculator:

    @staticmethod
    def calculate_moving_average(values: List[float], window: int) -> Optional[float]:
        return mean(values[-window:]) if len(values) >= window else None

    @staticmethod
    def calculate_rolling_std(values: List[float], window: int) -> Optional[float]:
        return stdev(values[-window:]) if len(values) >= window else None

    @staticmethod
    def calculate_high_low(values: List[float], window: int, high: bool = True) -> Optional[float]:
        subset = values[-window:]
        return max(subset) if high else min(subset) if len(subset) >= window else None

    @staticmethod
    def fill_moving_averages(market_data_list: Dict[str, List[MarketData]]) -> Dict[str, List[MarketData]]:
        for etf, data_list in market_data_list.items():
            # Lists to hold past values for rolling calculations
            volume_values = []
            close_values = []
            high_values = []
            low_values = []

            for i, data in enumerate(data_list):
                # Update rolling lists
                if data.etf_volume is not None:
                    volume_values.append(data.etf_volume)
                if data.etf_close is not None:
                    close_values.append(data.etf_close)
                if data.etf_high is not None:
                    high_values.append(data.etf_high)
                if data.etf_low is not None:
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
