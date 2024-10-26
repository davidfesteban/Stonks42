from typing import Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.modules.module import Module


def override(args):
    # Just a marker to remember forward comes from the parent nn.Module.
    pass


class ModelCreator(nn.Module):
    def __init__(self, enable_gpu: bool):
        super(ModelCreator, self).__init__()
        # Maybe as alternative lstm_layer = nn.LSTM(input_size=10, hidden_size=20, num_layers=2)
        self.device = torch.device('cuda' if enable_gpu and torch.cuda.is_available() else 'cpu')

        self.fc1 = nn.Linear(373, 128)  # 128 Neurons with 373 inputs
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.output = nn.Linear(32, 1)

        self.learning_ratio = 1e-5
        self.activation = nn.LeakyReLU(negative_slope=0.01)  # negative_slope is alpha
        self.criterion = nn.MSELoss()
        self.gradient_clip = 1.0

        print(self.device)

    @override
    def forward(self, x) -> Any:
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = self.output(x)  # Output for regression (no activation)
        return x

    def to_model_device(self) -> Module:
        return self.to(self.device)

    def optimizer(self, loaded_model: Module):
        return optim.Adam(loaded_model.parameters(), lr=self.learning_ratio)

    def save_model(self, loaded_model: Module, optimizer, path="model_checkpoint.pth"):
        torch.save({
            'model_state_dict': loaded_model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, path)
        print(f"Model saved to {path}")
