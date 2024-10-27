from typing import Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.modules.module import Module
from torch.optim.lr_scheduler import ReduceLROnPlateau


class ModelDefinitionGenA0(nn.Module):
    def __init__(self, enable_gpu: bool):
        super(ModelDefinitionGenA0, self).__init__()
        # Maybe as alternative lstm_layer = nn.LSTM(input_size=10, hidden_size=20, num_layers=2)
        self.device = torch.device('cuda' if enable_gpu and torch.cuda.is_available() else 'cpu')

        self.fc1 = nn.Linear(378, 378)  # 128 Neurons with 378 inputs
        self.fc2 = nn.Linear(378, 378)
        self.fc3 = nn.Linear(378, 128)
        self.fc4 = nn.Linear(128, 64)
        self.fc5 = nn.Linear(64, 32)
        self.output = nn.Linear(32, 1)

        self.learning_ratio = 1e-3
        self.activation = nn.LeakyReLU(negative_slope=0.01)  # negative_slope is alpha
        self.criterion = nn.MSELoss()
        self.gradient_clip = 1.0

        print(self.device)

    # Override
    def forward(self, x) -> Any:
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = self.activation(self.fc4(x))
        x = self.activation(self.fc5(x))
        x = self.output(x)  # Output for regression (no activation)
        return x

    def to_model_device(self) -> Module:
        return self.to(self.device)

    def optimizer(self, loaded_model: Module):
        return optim.AdamW(loaded_model.parameters(), lr=self.learning_ratio, betas=(0.8, 0.999), weight_decay=1e-3)

    def scheduler(self, loaded_optimizer):
        return ReduceLROnPlateau(loaded_optimizer, mode='min', factor=0.1, patience=10)
