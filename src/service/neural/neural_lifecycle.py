import time

import torch.nn.utils as nn_utils
from torch.nn.modules.module import Module
from torch.utils.data import DataLoader

from src.adapter.model.model_util import ModelUtil
from src.model.model_definition_gen_A0 import ModelDefinitionGenA0

# TODO: Wrapping timers

class NeuralLifecycle:

    @staticmethod
    def train_model(model_definition: ModelDefinitionGenA0, loaded_model: Module, data_loader: DataLoader, optimizer,
                    scheduler,
                    epochs: int,
                    callback):
        loaded_model.train()  # Set model to training mode
        for epoch in range(epochs):
            running_loss_counter = 0.0
            item_counter = 0

        # Dictionary to store time taken for each operation
            timers = {
                "Zero Grad": 0.0,
                "Forward Pass": 0.0,
                "Backward Pass": 0.0,
                "Opt Step": 0.0,
                "Finishing Step": 0.0
            }

            for batch_index, (features, expected) in enumerate(data_loader):
                # Zero Grad
                start_time = time.time()
                optimizer.zero_grad()
                timers["Zero Grad"] += time.time() - start_time

                # Forward Pass
                start_time = time.time()
                outputs = loaded_model(features)
                loss = model_definition.criterion(outputs, expected)
                timers["Forward Pass"] += time.time() - start_time

                # Backward Pass
                start_time = time.time()
                loss.backward()
                nn_utils.clip_grad_norm_(loaded_model.parameters(), max_norm=model_definition.gradient_clip)
                timers["Backward Pass"] += time.time() - start_time

                # Opt Step
                start_time = time.time()
                optimizer.step()
                timers["Opt Step"] += time.time() - start_time

                # Finishing Step (accumulating loss)
                start_time = time.time()
                running_loss_counter += loss.item()
                item_counter += 1
                timers["Finishing Step"] += time.time() - start_time

                features.detach()
                expected.detach()

            # Calculate and print average loss per epoch
            avg_loss = running_loss_counter / item_counter
            scheduler.step(avg_loss)

            # Print timer results
            print("\nTiming Results:")
            for operation, total_time in timers.items():
                print(f"{operation}: {total_time:.4f} seconds")

            if callback:
                callback(epoch + 1, avg_loss)

            #TODO Add into call back also:
            if epoch % 100 == 0:
                ModelUtil.save_model(loaded_model=loaded_model, optimizer=optimizer, last_error=avg_loss)

            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}")

    # @staticmethod
    # def evaluate_model(model, data_loader, criterion, device):
    #    model.eval()  # Set model to evaluation mode
    #    val_loss_counter = 0.0
    #    correct_predictions = 0
    #    total_predictions = 0
    #
    #    with torch.no_grad():  # Disable gradient calculation
    #        for features, expected in data_loader:
    #            features, expected = features.to(device), expected.to(device)
    #
    #            # Forward pass
    #            outputs = model(features)
    #            val_loss = criterion(outputs, expected)
    #
    #            # Accumulate validation loss
    #            val_loss_counter += val_loss.item()
    #
    #            # Calculate accuracy if this is a classification model
    #            _, predicted = torch.max(outputs, 1)  # Assumes outputs are logits for classification
    #            correct_predictions += (predicted == expected).sum().item()
    #            total_predictions += expected.size(0)
    #
    #    avg_val_loss = val_loss_counter / len(data_loader)
    #    accuracy = correct_predictions / total_predictions
    #    print(f"Validation Loss: {avg_val_loss:.4f}, Accuracy: {accuracy:.2%}")
