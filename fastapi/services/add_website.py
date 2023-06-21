from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from base import session
from db import Websites, IPs, Websites_has_IPs, Responses
from models.websitesModels import WebsiteModel
import requests
import socket
import datetime
import http

router = APIRouter()

@router.post("/add-website")
def add_website(website: WebsiteModel):
    try:
        if website.hostname[0:4] != "http":
            website_check = "https://" + website.hostname
            try:
                request = requests.get(website_check, stream=True)
                website.hostname = "https://" + website.hostname
            except:
                website.hostname = "http://" + website.hostname
        
        if website.hostname[-1] != "/":
            website.hostname = website.hostname + "/"
        
        status = 0
        request = ""
        source = ""

        # See if url is valid
        try:
            request = requests.get(str(website.hostname), stream=True)
            status = int(request.status_code)
        except Exception as e:
            print("Wrong url!") #Return response
            return JSONResponse(status_code=400, content={"message": "Wrong url!"})
        
        # See if I can get IP from website
        if status == 200:
            try:
                s = socket.fromfd(request.raw.fileno(), socket.AF_INET, socket.SOCK_STREAM)
                source = str(s.getpeername()[0])
            except Exception as e:
                print("Couldn't get IP from website!") #Return response
                return JSONResponse(status_code=400, content={"message": "Couldn't get IP from website!"})
        
        # Adding website and IP to tables
        newWebsite = False
        newIP = False

        if session.query(Websites).filter(Websites.hostname == website.hostname).first() is None:
            newWebsite = True
            new_website = Websites(website.hostname)
            session.add(new_website)

        if session.query(IPs).filter(IPs.ip == source).first() is None:
            newIP = True
            new_ip = IPs(source)
            session.add(new_ip)
            
        
        if newIP or newWebsite:
            session.commit()
            new_entry = Websites_has_IPs.insert().values(
                Websites_hostname=website.hostname,
                IPs_ip=source
            )
            session.execute(new_entry)

        if newIP or newWebsite:
            session.commit() 
            respond = Responses(status, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), source)
            session.add(respond)
            session.commit()
            return JSONResponse(status_code=201, content={"message": "Website and/or IP has been added to database!"})
        else:
            return Response(status_code=http.HTTPStatus.NOT_MODIFIED)

    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"message": "Something went wrong!"})