from typing import Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.modules.module import Module

class ModelUtil:

    @staticmethod
    def save_model(loaded_model: Module, optimizer, path="model_checkpoint.pth"):
        torch.save({
            'model_state_dict': loaded_model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, path)
        print(f"Model saved to {path}")
