import os
from sqlalchemy import create_engine

current_dir = os.path.dirname(os.path.abspath(__file__))
database_url = f"sqlite:///{os.path.join(current_dir, 'messages.db')}"
engine = create_engine(database_url, echo=True)