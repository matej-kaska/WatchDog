from fastapi import APIRouter
from fastapi.responses import JSONResponse
from base import session
from db import Websites, Responses, Websites_has_IPs
from models.websitesModels import IPModel
import datetime
import requests

router = APIRouter()

@router.post("/check-status")
def check_status(ip: IPModel):
    try:        
        hostname = session.query(Websites).join(Websites_has_IPs).filter(Websites_has_IPs.c.IPs_ip == ip.ip).first().hostname
        if hostname[0:5] == "https":
            ip_req = "https://" + ip.ip
        else:
            ip_req = "http://" + ip.ip

        request = requests.get(ip_req, stream=True, verify=False)
        status = int(request.status_code)
        date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        respond = Responses(status, date, ip.ip)
        session.add(respond)
        session.commit()
        return JSONResponse(status_code=200, content={"ip": ip.ip, "status": status, "date": date})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"error_message": "Something went wrong!"})