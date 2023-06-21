import requests
import socket
import datetime
from db import Websites, IPs, Responses
from base import Session, engine, Base

# Generate database schema
Base.metadata.create_all(engine)

# Create a new session
session = Session()

# get status code of every website in db
for web in session.query(Websites).all():
    try:
        r = requests.get(str(web.hostname), stream=True)
        status = int(r.status_code)
        s = socket.fromfd(r.raw.fileno(), socket.AF_INET, socket.SOCK_STREAM)
        source = str(s.getpeername()[0])
        
        if(session.query(IPs).filter(IPs.ip == source).first() is None):
            print("Checking: " + web.hostname + " " + str(status))
            ip = IPs(source, web)
            session.add(ip)
            session.commit()
        else:
            print("Checking: " + web.hostname + " " + str(status) + " ip is in db")
            
        respond = Responses(status, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), source)
        session.add(respond)
        session.commit()
    except:
        print(web.hostname + " was not found")