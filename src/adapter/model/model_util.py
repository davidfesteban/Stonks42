from pathlib import Path

import torch
from torch.nn.modules.module import Module


class ModelUtil:

    @staticmethod
    def save_model(loaded_model: Module, optimizer, name="A01", last_error=0.0):
        total_path = Path(__file__).parent.parent.parent.parent / "output" / "tmp" / (name + '.pth')
        torch.save({
            'last_error': last_error,
            'model_state_dict': loaded_model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, total_path)
        print(f"Model saved to {total_path}")
