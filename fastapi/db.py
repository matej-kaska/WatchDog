from sqlalchemy import Column, Table, VARCHAR, ForeignKey, Integer, SMALLINT, DATETIME
from sqlalchemy.orm import relationship
from base import Base


# Joining table Websites_has_IPs
Websites_has_IPs = Table("Websites_has_IPs", Base.metadata,
    Column("Websites_hostname", VARCHAR, ForeignKey('Websites.hostname'), primary_key=True),
    Column("IPs_ip", VARCHAR, ForeignKey('IPs.ip'), primary_key=True))

# Website: hostname
class Websites(Base):
    __tablename__ = 'Websites'
    hostname = Column(VARCHAR, nullable=False, primary_key=True)
    
    def __init__(self, hostname: str):
        self.hostname = hostname

# IPs: ip, Websites
class IPs(Base):
    __tablename__ = 'IPs'
    ip = Column(VARCHAR, nullable=False, primary_key=True)
    Website = relationship("Websites", secondary=Websites_has_IPs, backref="Websites_has_IPs")
    
    def __init__(self, ip: str):
        self.ip = ip

# Responses: id, code, time, IP_ip
class Responses(Base):
    __tablename__ = 'Responses'
    id = Column(Integer, nullable=False, primary_key=True)
    code = Column(SMALLINT, nullable=False)
    time = Column(DATETIME, nullable=False)
    IP_ip = Column(VARCHAR, ForeignKey('IPs.ip'))
    
    def __init__(self, code: int, time: str, IP_ip: str):
        self.code = code
        self.time = time
        self.IP_ip = IP_ip
