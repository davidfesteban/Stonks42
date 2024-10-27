import torch.nn.utils as nn_utils
from torch.nn.modules.module import Module
from torch.utils.data import DataLoader

from src.model.model_definition_gen_A0 import ModelDefinitionGenA0


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

            for batch_index, (features, expected) in enumerate(data_loader):
                features, expected = features.to(model_definition.device), expected.to(model_definition.device)

                optimizer.zero_grad()

                # Forward pass
                outputs = loaded_model(features)
                loss = model_definition.criterion(outputs, expected)

                loss.backward()
                nn_utils.clip_grad_norm_(loaded_model.parameters(), max_norm=model_definition.gradient_clip)

                optimizer.step()

                # Accumulate loss
                running_loss_counter += loss.item()
                item_counter += 1

            # Calculate and print average loss per epoch
            avg_loss = running_loss_counter / item_counter
            scheduler.step(avg_loss)

            if callback:
                callback(epoch + 1, avg_loss)
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
