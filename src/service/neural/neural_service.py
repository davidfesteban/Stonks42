from torch.utils.data import DataLoader

from src.adapter.metric.loss_line_chart import LossLineChart
from src.adapter.model.model_util import ModelUtil
from src.adapter.mongo.mongo_connector import MongoConnector
from src.adapter.mongo.mongo_data_pair_mapper import MongoDataPairMapper
from src.adapter.mongo.progressive_mongo_dataset import ProgressiveMongoDataset
from src.model.model_definition_gen_A0 import ModelDefinitionGenA0
from src.service.neural.neural_lifecycle import NeuralLifecycle


class NeuralService:
    _collection = "Stonks_Full_30_Oct_2024"

    def run(self):
        # Initialize MongoDB connection and Model Definition
        mongo_connector = MongoConnector()
        model_definition = ModelDefinitionGenA0(mongo_connector.count_input_expected_size(NeuralService._collection),
                                                enable_gpu=True)

        # Load the model, optimizer and LR Scheduler
        loaded_model = model_definition.to_model_device()
        optimizer = model_definition.optimizer(loaded_model)
        scheduler = model_definition.scheduler(optimizer)

        # Initialize MongoDB Cursor and dataset
        progressive_mongo_cursor = ProgressiveMongoDataset(client=mongo_connector,
                                                           query_function=lambda
                                                               client: client.find_by_collection_ordered_asc(
                                                               NeuralService._collection),
                                                           query_count=lambda client: client.count_data_pairs(
                                                               NeuralService._collection),
                                                           mapper=lambda document: MongoDataPairMapper.map_to_data_pair(
                                                               document, model_definition.device))

        data_loader = DataLoader(progressive_mongo_cursor, batch_size=model_definition.dataloader_batch, num_workers=0,
                                 pin_memory=True)

        # Initialize Callback for Plot
        loss_chart = LossLineChart()

        # Start Training
        NeuralLifecycle.train_model(model_definition, loaded_model, data_loader, optimizer, scheduler, 100000,
                                    callback=loss_chart.add)

        # Reactive plotting and finishing if not plotted values
        loss_chart.plot()

        # Save Training Model Last Result
        ModelUtil.save_model(loaded_model=loaded_model, optimizer=optimizer, name='A01')
