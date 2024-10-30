from datetime import datetime, timedelta
from typing import List, Dict, Optional

from src.dto.market_data import MarketData


class MarketDataConverter:

    @staticmethod
    def trim_to_current_etf(data: Dict[str, List[MarketData]]) -> Dict[str, List[MarketData]]:
        market_dict = dict(data)
        for key in market_dict:
            market_dict[key].sort(key=lambda market: market.date)

        market_data = market_dict.get('current_etf', [])
        if not market_data:
            return {}

        min_date = market_data[0].date
        max_date = market_data[-1].date

        for key in market_dict:
            market_dict[key] = [market for market in market_dict[key] if min_date <= market.date <= max_date]

        return market_dict

    @staticmethod
    def forward_and_fill_gaps(data: Dict[str, List[MarketData]]) -> Dict[str, List[MarketData]]:
        # Clone the data to avoid modifying the original input
        market_dict = dict(data)
        current_etf_market_data = market_dict.get('current_etf', [])
        if not current_etf_market_data:
            return market_dict  # Return as-is if `current_etf` has no data

        # Get the minimum and maximum dates from the 'current_etf' data
        min_date = current_etf_market_data[0].date
        max_date = current_etf_market_data[-1].date

        for key, market_data_list in market_dict.items():
            if not market_data_list:
                continue

            market_data_list.sort(key=lambda market: market.date)
            filled_data = []

            current_date = datetime.strptime(str(min_date), '%Y%m%d')
            end_date = datetime.strptime(str(max_date), '%Y%m%d')

            index = 0
            last_known_data: Optional[MarketData] = None

            while current_date <= end_date:
                current_date_int = int(current_date.strftime('%Y%m%d'))

                if index < len(market_data_list) and market_data_list[index].date == current_date_int:
                    # If there is a matching entry, add it to filled_data
                    filled_data.append(market_data_list[index])
                    last_known_data = market_data_list[index]  # Update last known data for forward-filling
                    index += 1
                else:
                    if last_known_data is None:
                        filled_data.append(MarketData(
                            date=current_date_int,
                            day_of_week=current_date.weekday()
                        ).fill_na_with_zero())
                    elif (current_date - datetime.strptime(str(last_known_data.date), '%Y%m%d')).days <= 2:
                        filled_data.append(MarketData(
                            date=current_date_int,
                            day_of_week=current_date.weekday(),
                            etf_open=last_known_data.etf_open,
                            etf_high=last_known_data.etf_high,
                            etf_low=last_known_data.etf_low,
                            etf_close=last_known_data.etf_close,
                            etf_volume=last_known_data.etf_volume,
                        ).fill_na_with_zero())
                    else:
                        filled_data.append(MarketData(
                            date=current_date_int,
                            day_of_week=current_date.weekday()
                        ).fill_na_with_zero())

                current_date += timedelta(days=1)

            market_dict[key] = filled_data

        return market_dict
