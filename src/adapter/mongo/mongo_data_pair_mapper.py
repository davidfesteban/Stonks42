import torch

from src.dto.data_pair import DataPair


class MongoDataPairMapper:
    @staticmethod
    def map_to_data_pair(document, device, definition=-1):
        data_pair = DataPair(**document)

        if definition == -1:
            data_pair_expected = data_pair.expected
        else:
            data_pair_expected = [data_pair.expected[definition]]

        feature_tensor = torch.tensor(data_pair.inputs, dtype=torch.float32).to(device)
        expected_tensor = torch.tensor(data_pair_expected, dtype=torch.float32).to(device)
        return feature_tensor, expected_tensor
