import pandas as pd
import yfinance
from pandas import Timestamp

from src.dto.time_point import TimePoint
from typing import Union, Dict, Any

class YahooBridge:
    @staticmethod
    def grab_normalised_dataframes_by_field(time_point: TimePoint):
        min_head: Union[Timestamp, None] = None
        max_head: Union[Timestamp, None] = None
        result: Dict[str, pd.DataFrame] = {}
        for field, ticker in time_point.field_tickers.items():
            # dataframe_history = yfinance.Ticker(ticker).history(period="max", repair=True)
            dataframe_history = yfinance.Ticker(ticker).history(start="2024-10-01")
            dataframe_history = dataframe_history.tz_convert("UTC")

            if field == "current_etf":
                min_head = dataframe_history.index.min()
                max_head = dataframe_history.index.max()

            # Generate the full date range between min_head and max_head
            full_date_range = pd.date_range(start=min_head, end=max_head, freq='D', tz='UTC')

            # Find missing dates by comparing the full range to existing dates
            missing_dates = full_date_range.difference(dataframe_history.index)

            # Create a DataFrame for missing dates with NaN values for columns
            missing_data = pd.DataFrame(index=missing_dates, columns=dataframe_history.columns)

            # Append missing dates to the original data
            dataframe_history = pd.concat([dataframe_history, missing_data]).sort_index()

            # Fill any missing data
            dataframe_history = dataframe_history.fillna(method='ffill').fillna(0)
            result[field] = dataframe_history
            print(dataframe_history.to_json(orient="records", date_format="iso"))

        return result