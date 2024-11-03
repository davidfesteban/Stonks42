##TODO make it reactive!!
# app = FastAPI()

from src.service.neural.neural_service import NeuralService


# TODO: Add NEAT
def main():
    # ScrapService().run()
    NeuralService().run()
    # NeuralService().predict(date=20241014)


if __name__ == "__main__":
    main()
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
