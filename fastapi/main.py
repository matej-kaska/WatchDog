from base import engine, Base
from fastapi import FastAPI
from services import list_websites
from uvicorn import run

app = FastAPI()

# Generate database schema
Base.metadata.create_all(engine)

# Include routers
app.include_router(list_websites.router)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5001)