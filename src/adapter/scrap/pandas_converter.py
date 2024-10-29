from typing import Dict, List

import pandas as pd

from src.dto.market_data import MarketData
from src.dto.time_point import TimePoint


class PandasConverter:
    @staticmethod
    def deserialize(market_data_panda: Dict[str, pd.DataFrame]) -> List[TimePoint]:
        result: List[TimePoint] = []

        # Normalize each DataFrame index to remove time components
        for df in market_data_panda.values():
            df.index = df.index.normalize()

        # Generate a set of all unique dates across DataFrames
        all_dates = sorted(
            set(date.normalize() for df in market_data_panda.values() for date in df.index)
        )

        for date in all_dates:
            time_point = TimePoint()
            for field, dataframe in market_data_panda.items():
                if date in dataframe.index:
                    row = dataframe.loc[date]

                    # Calculate moving averages and other indicators by slicing directly
                    avg_5_vol = dataframe.loc[:date, 'Volume'].tail(5).mean()  # Last 5 days
                    avg_10_vol = dataframe.loc[:date, 'Volume'].tail(10).mean()  # Last 10 days
                    avg_20_vol = dataframe.loc[:date, 'Volume'].tail(20).mean()
                    avg_30_vol = dataframe.loc[:date, 'Volume'].tail(30).mean()
                    avg_50_vol = dataframe.loc[:date, 'Volume'].tail(50).mean()
                    avg_100_vol = dataframe.loc[:date, 'Volume'].tail(100).mean()
                    avg_200_vol = dataframe.loc[:date, 'Volume'].tail(200).mean()

                    avg_5_close = dataframe.loc[:date, 'Close'].tail(5).mean()
                    avg_10_close = dataframe.loc[:date, 'Close'].tail(10).mean()
                    avg_20_close = dataframe.loc[:date, 'Close'].tail(20).mean()
                    avg_30_close = dataframe.loc[:date, 'Close'].tail(30).mean()
                    avg_50_close = dataframe.loc[:date, 'Close'].tail(50).mean()
                    avg_100_close = dataframe.loc[:date, 'Close'].tail(100).mean()
                    avg_200_close = dataframe.loc[:date, 'Close'].tail(200).mean()

                    week_52_high = dataframe.loc[:date, 'High'].tail(252).max()  # Last 52 weeks
                    week_52_low = dataframe.loc[:date, 'Low'].tail(252).min()

                    # Volatility (standard deviation of returns)
                    volatility_10_days = dataframe.loc[:date, 'Close'].pct_change().dropna().tail(10).std()
                    volatility_20_days = dataframe.loc[:date, 'Close'].pct_change().dropna().tail(20).std()
                    volatility_30_days = dataframe.loc[:date, 'Close'].pct_change().dropna().tail(30).std()

                    # Construct MarketData instance
                    market_data = MarketData(
                        date=int(date.timestamp()),
                        day_of_week=date.dayofweek,
                        etf_open=row.get("Open"),
                        etf_close=row.get("Close"),
                        etf_low=row.get("Low"),
                        etf_high=row.get("High"),
                        etf_volume=row.get("Volume"),
                        average_5_days_volume=avg_5_vol,
                        average_10_days_volume=avg_10_vol,
                        average_20_days_volume=avg_20_vol,
                        average_30_days_volume=avg_30_vol,
                        average_50_days_volume=avg_50_vol,
                        average_100_days_volume=avg_100_vol,
                        average_200_days_volume=avg_200_vol,
                        average_5_days_close=avg_5_close,
                        average_10_days_close=avg_10_close,
                        average_20_days_close=avg_20_close,
                        average_30_days_close=avg_30_close,
                        average_50_days_close=avg_50_close,
                        average_100_days_close=avg_100_close,
                        average_200_days_close=avg_200_close,
                        etf_week_52_low=week_52_low,
                        etf_week_52_high=week_52_high,
                        volatility_10_days=volatility_10_days,
                        volatility_20_days=volatility_20_days,
                        volatility_30_days=volatility_30_days
                    )

                    setattr(time_point, field, market_data)
                else:
                    print(f"Error date not found! {field} {date}")

            result.append(time_point)

        return result
