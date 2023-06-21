from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from base import session
from db import Websites, IPs, Websites_has_IPs
from models.websitesModels import Payload
import json

router = APIRouter()

@router.get("/api/list")
def api_list_websites():
    try:
        websites = session.query(Websites, IPs).select_from(Websites).join(Websites_has_IPs).join(IPs).all()
        list_websites = [{"hostname": web.Websites.hostname, "ip": web.IPs.ip} for web in websites]
        list_websites = json.dumps(list_websites, indent=4)
        return Response(content=list_websites, media_type="application/json")
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"error_message": "Something went wrong!"})