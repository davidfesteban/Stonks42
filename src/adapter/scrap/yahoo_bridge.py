from collections import defaultdict
from typing import Dict, List, Type

import yfinance

from src.dto.market_data import MarketData
from src.dto.time_point import TimePoint


class YahooBridge:

    @staticmethod
    def grab_normalised_dataframes_by_field(time_point_class: Type[TimePoint]) -> Dict[str, List[MarketData]]:
        result: Dict[str, List[MarketData]] = defaultdict(list)

        for field, ticker in time_point_class.get_field_tickers().items():
            # dataframe_history = yfinance.Ticker(ticker).history(start="2024-10-25")
            dataframe_history = yfinance.Ticker(ticker).history(period="max", repair=True)
            dataframe_history = dataframe_history.tz_convert("UTC")

            # Iterate over each row in the DataFrame
            for date, row in dataframe_history.iterrows():
                # Convert the date to an integer in YYYYMMDD format
                date_as_int = int(date.strftime('%Y%m%d'))

                # Create a MarketData object for this row
                market_data = MarketData(
                    date=date_as_int,
                    day_of_week=date.weekday(),
                    etf_open=row['Open'],
                    etf_high=row['High'],
                    etf_low=row['Low'],
                    etf_close=row['Close'],
                    etf_volume=row['Volume']
                )

                # Append MarketData to the list for this field
                result[field].append(market_data)
                # market_data_list.append(market_data)
        return result
