##TODO make it reactive!!
# app = FastAPI()
from torch.utils.data import DataLoader

from model_creator import ModelCreator
from mogno_dataset_tensor import MongoDataset
from mongo_connector import MongoConnector
from neural_lifecycle import NeuralLifecycle

# Initialize MongoDB connection and dataset
mongo_connector = MongoConnector('dataPair')
mongo_dataset_tensor = MongoDataset(mongo_connector.find_by_topic_ordered_asc("StonksV2"))
data_loader = DataLoader(mongo_dataset_tensor, batch_size=64)

# Initialize model and optimizer
model_definition = ModelCreator(enable_gpu=True)
loaded_model = model_definition.to_model_device()
optimizer = model_definition.optimizer(loaded_model)

# Training parameters
epochs = 100

NeuralLifecycle.train_model(model_definition, loaded_model, data_loader, optimizer, 100)
model_definition.save_model(loaded_model, optimizer)

# if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
