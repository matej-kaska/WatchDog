from uvicorn import run
from main import app

if __name__ == "__main__":
    run("debug_server:app", host="0.0.0.0", port=5001, reload=True)