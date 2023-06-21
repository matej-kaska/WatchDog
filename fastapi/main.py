from base import engine, Base
from fastapi import FastAPI
from services import list_websites, add_website, website
from fastapi.staticfiles import StaticFiles
from uvicorn import run

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Generate database schema
Base.metadata.create_all(engine)

# Include routers
app.include_router(list_websites.router)
app.include_router(add_website.router)
app.include_router(website.router)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5001)