from typing import Any, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.modules.module import Module
from torch.optim.lr_scheduler import ReduceLROnPlateau

# Change DataLoad batch from 64 to 128.
# Reduce the Dense Layer complexity
# Introduce LSTM
# And maybe, change AdamW by LAMB
# And maybe disable the Queue from CSV
# And maybe install CUDA

class ModelDefinitionGenA0(nn.Module):

    def __init__(self, input_expected_count: Tuple[int, int], enable_gpu: bool):
        super(ModelDefinitionGenA0, self).__init__()
        # Maybe as alternative lstm_layer = nn.LSTM(input_size=10, hidden_size=20, num_layers=2)
        self.device = torch.device('cuda' if enable_gpu and torch.cuda.is_available() else 'cpu')
        print(self.device)
        # input_expected_count
        self.layers = nn.ModuleList([

            nn.Linear(702, 256),
            nn.Linear(256, 128),
            nn.Linear(128, 64),
            nn.Linear(64, 32),
            nn.Linear(32, 1)
        ])


        self.learning_ratio = 1e-3
        self.activation = nn.LeakyReLU(negative_slope=0.01)  # negative_slope is alpha
        self.criterion = nn.MSELoss()
        self.gradient_clip = 1.0

        self.dataloader_batch = 128

        print(self.device)

    # Override
    def forward(self, x) -> Any:
        for layer in self.layers[:-1]:
            x = self.activation(layer(x))

        x = self.layers[-1](x)  # Output for regression (no activation)
        return x

    def to_model_device(self) -> Module:
        return self.to(self.device)

    def optimizer(self, loaded_model: Module):
        return optim.AdamW(loaded_model.parameters(), lr=self.learning_ratio, betas=(0.8, 0.999), weight_decay=1e-3)

    def scheduler(self, loaded_optimizer):
        return ReduceLROnPlateau(loaded_optimizer, mode='min', factor=0.1, patience=10)
