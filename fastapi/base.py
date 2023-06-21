from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://root:password@database:3306/WatchDog")
Session = sessionmaker(bind=engine)

# Create a new session
session = Session()

Base = declarative_base()