from torch.utils.data import DataLoader

from src.adapter.model.model_util import ModelUtil
from src.adapter.mongo.mongo_tensor_cursor import MongoTensorCursor
from src.adapter.mongo.tensor_cache_queue import TensorCacheQueue
from src.model.model_definition_gen_A0 import ModelDefinitionGenA0

from src.adapter.mongo.mongo_connector import MongoConnector
from src.service.neural.neural_lifecycle import NeuralLifecycle
from torch.optim.lr_scheduler import ReduceLROnPlateau

class NeuralService:
    def run(self):
        # Initialize model and optimizer
        model_definition = ModelDefinitionGenA0(enable_gpu=True)
        loaded_model = model_definition.to_model_device()
        optimizer = model_definition.optimizer(loaded_model)
        scheduler = model_definition.scheduler(optimizer)

        # Initialize MongoDB connection and dataset
        mongo_connector = MongoConnector()
        mongo_tensor_cursor = TensorCacheQueue(mongo_connector.find_by_collection_ordered_asc("StocksV2"))
        data_loader = DataLoader(mongo_tensor_cursor, batch_size=64, num_workers=0, pin_memory=True)

        # Initialize Callback for Plot

        # Start Training
        NeuralLifecycle.train_model(model_definition, loaded_model, data_loader, optimizer, scheduler, 100000)

        # Save Training Model Result
        ModelUtil.save_model(loaded_model=loaded_model, optimizer=optimizer)

