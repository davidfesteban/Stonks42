from src.adapter.mongo.mongo_connector import MongoConnector
from src.adapter.scrap.data_pair_converter import DataPairConverter
from src.adapter.scrap.pandas_converter import PandasConverter
from src.adapter.scrap.yahoo_bridge import YahooBridge
from src.dto.time_point import TimePoint

# TODO: Make it reactive or secuencial. Too much memory here!

class ScrapService:
    def run(self):
        dataframe_dict = YahooBridge.grab_normalised_dataframes_by_field(TimePoint())
        time_point_list = PandasConverter.deserialize(dataframe_dict)
        data_pair_list = DataPairConverter.convert_to_data_pair(time_point_list)
        MongoConnector().save_data_pairs("StonksV3", data_pair_list)
