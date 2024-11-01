import torch

from src.dto.data_pair import DataPair


class MongoDataPairMapper:
    @staticmethod
    def map_to_data_pair(document, device):
        data_pair = DataPair(**document)
        feature_tensor = torch.tensor(data_pair.inputs, dtype=torch.float32).to(device)
        expected_tensor = torch.tensor(data_pair.expected, dtype=torch.float32).to(device)
        return feature_tensor, expected_tensor
