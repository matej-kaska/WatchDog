from base import engine, Base
from fastapi import FastAPI
from services import add_website, list_websites, website, check_website, api_list_websites, api_responses
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
app.include_router(check_website.router)
app.include_router(api_list_websites.router)
app.include_router(api_responses.router)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5001)