from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from base import session
from db import Websites, IPs, Websites_has_IPs, Responses
import json

router = APIRouter()

@router.get("/api/website/{hostname:path}")
def api_responses(hostname: str):
    try:
        websites = session.query(IPs.ip, Responses.code).select_from(IPs).join(Websites_has_IPs).join(Responses).join(Websites).filter(Websites.hostname == hostname).all()
        list_websites = [{"ip": web[0], "status": web[1]} for web in websites]
        list_websites = json.dumps(list_websites, indent=4)
        return Response(content=list_websites, media_type="application/json")
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"error_message": "Something went wrong!"})