from uvicorn import run

app = FastAPI()

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5001)