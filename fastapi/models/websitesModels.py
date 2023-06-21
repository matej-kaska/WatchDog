from pydantic import BaseModel

class WebsiteModel(BaseModel):
    hostname: str

class IPModel(BaseModel):
    ip: str

class Payload(BaseModel):
    data: str = ""