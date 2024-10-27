##TODO make it reactive!!
# app = FastAPI()
from torch.utils.data import DataLoader

from model_creator import ModelCreator
from mongo_dataset_tensor import MongoDatasetTensorCache
from mongo_connector import MongoConnector
from neural_lifecycle import NeuralLifecycle
from torch.optim.lr_scheduler import ReduceLROnPlateau

# TODO: Add NEAT
def main():
    # Initialize MongoDB connection and dataset
    mongo_connector = MongoConnector('dataPair')
    mongo_dataset_tensor = MongoDatasetTensorCache(mongo_connector.find_by_topic_ordered_asc("StocksV2"))
    data_loader = DataLoader(mongo_dataset_tensor, batch_size=64, num_workers=0, pin_memory=True)

    # Initialize model and optimizer
    model_definition = ModelCreator(enable_gpu=True)
    loaded_model = model_definition.to_model_device()
    optimizer = model_definition.optimizer(loaded_model)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)

    NeuralLifecycle.train_model(model_definition, loaded_model, data_loader, optimizer, scheduler, 150000)
    model_definition.save_model(loaded_model, optimizer)

if __name__ == "__main__":
    main()
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
