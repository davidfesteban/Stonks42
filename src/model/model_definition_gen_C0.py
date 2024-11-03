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

class ModelDefinitionGenC0(nn.Module):
    available_collections = ["Stonks_Full_3_Nov_2024_PCT"]

    def __init__(self, input_expected_count: Tuple[int, int], enable_gpu: bool):
        super(ModelDefinitionGenC0, self).__init__()

        self.device = torch.device('cuda' if enable_gpu and torch.cuda.is_available() else 'mps' if enable_gpu and torch.backends.mps.is_available() else 'cpu')
        print(self.device)

        # LSTM layer
        self.lstm = nn.LSTM(input_size=702, hidden_size=512, num_layers=2, batch_first=True)

        # Fully connected layers
        self.fc_layers = nn.Sequential(
            nn.Linear(512, 256),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(256, 128),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(128, 64),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(64, 32),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(32, 3)  # Output layer
        )

        self.learning_ratio = 1e-3
        self.criterion = nn.MSELoss()
        self.gradient_clip = 1.0
        self.dataloader_batch = 128

    def forward(self, x) -> Any:
        # Ensure x is shaped (batch_size, 1, input_size)
        x = x.unsqueeze(1)  # Adding sequence length dimension for LSTM compatibility

        # Pass through LSTM
        lstm_out, _ = self.lstm(x)
        lstm_out = lstm_out[:, -1, :]  # Take last time step output for fully connected layers

        # Pass through fully connected layers
        out = self.fc_layers(lstm_out)
        return out


    def to_model_device(self) -> Module:
        return self.to(self.device)

    def optimizer(self, loaded_model: Module):
        return optim.AdamW(loaded_model.parameters(), lr=self.learning_ratio, betas=(0.85, 0.999), weight_decay=1e-3)

    def scheduler(self, loaded_optimizer):
        return ReduceLROnPlateau(loaded_optimizer, mode='min', factor=0.1, patience=10)
