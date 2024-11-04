##TODO make it reactive!!
# app = FastAPI()

from src.service.neural.neural_service import NeuralService
from src.service.scrap.scrap_service import ScrapService


# TODO: LSTM, TRANSFORMERS vs TGN TCN
# TODO: Fix LSTM size
# TODO: General training and then focused training
# TODO: Increase dataset
# TODO: Add NEAT

def main():
    ScrapService().from_date()
    # NeuralService().run()
    # NeuralService().predict(date=20241031)


if __name__ == "__main__":
    main()
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
