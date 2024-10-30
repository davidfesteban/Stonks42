from src.adapter.mongo.mongo_connector import MongoConnector
from src.adapter.scrap.data_pair_converter import DataPairConverter
from src.adapter.scrap.market_data_converter import MarketDataConverter
from src.adapter.scrap.moving_average_calculator import MovingAverageCalculator

from src.adapter.scrap.time_point_converter import TimePointConverter
from src.adapter.scrap.yahoo_bridge import YahooBridge
from src.dto.time_point import TimePoint

# TODO: Make it reactive or secuencial. Too much memory here!

class ScrapService:
    def run(self):
        market_dict = YahooBridge.grab_normalised_dataframes_by_field(TimePoint)
        trimmed_dict = MarketDataConverter.trim_to_current_etf(market_dict)
        filled_basic_dict = MarketDataConverter.forward_and_fill_gaps(trimmed_dict)
        filled_total_dict = MovingAverageCalculator.fill_moving_averages(filled_basic_dict)
        time_point_list = TimePointConverter.fill_none_and_convert(filled_total_dict)
        data_pair_list = DataPairConverter.convert_to_data_pair(time_point_list)

        MongoConnector().save_data_pairs("StonksV3", data_pair_list)
