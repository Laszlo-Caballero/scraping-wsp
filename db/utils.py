from db.engine import engine
from db import model
from sqlalchemy.orm import sessionmaker

def create_tables():
    model.Base.metadata.create_all(engine)

def drop_tables():
    model.Base.metadata.drop_all(engine)

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()