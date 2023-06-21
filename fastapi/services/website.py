import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from base import session
from db import IPs, Responses, Websites_has_IPs
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Include templates
templates = Jinja2Templates(directory="templates")

@router.get("/website/{hostname:path}")
def website(request: Request, hostname: str):
    print(hostname)
    try:
        ips_query = session.query(IPs).join(Websites_has_IPs).filter(Websites_has_IPs.c.Websites_hostname == hostname).all()
        ips = [i.ip for i in ips_query]
        responses = []
        last_response = []
        chart_data = []
        for ip in ips:
            responses_query = session.query(Responses).filter(Responses.IP_ip == ip).all()
            ip_responses = [(res.IP_ip, res.code, res.time) for res in responses_query]
            responses.append([*ip_responses])
            last_response.append([*ip_responses[-1]])
            chart_responses = [("DOWN" if res.code in [404, 502, 503, 504] else "UP", str(res.time)) for res in responses_query]
            for response in chart_responses:
                chart_data.append({"y": response[0], "x": response[1]})
        context = {"request": request, "responses": responses, "last_response": last_response, "chart_data": json.dumps(chart_data)}
        return templates.TemplateResponse("website.html", context)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"error_message": "Something went wrong!"})