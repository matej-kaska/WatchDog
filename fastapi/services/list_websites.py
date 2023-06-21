from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from base import session
from db import Websites
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Include templates
templates = Jinja2Templates(directory="templates")

@router.get("/")
def list_websites(request: Request):
    try:
        websites = session.query(Websites).all()
        list_websites = [web.hostname for web in websites]
        context = {"request": request, "websites": list_websites}
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"error_message": "Something went wrong!"})