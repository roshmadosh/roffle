import sqlalchemy as db
from typing import List
from models.Message import Message
from dotenv import load_dotenv 
import os



# init
load_dotenv()
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
schema_name = 'capstone'

class DAO:
    def __init__(self):
        engine = db.create_engine(
            f"mysql+pymysql://{username}:{password}@{url}/{schema_name}", echo=False)

        self.conn = engine.connect()

    def execute_query(self, query: str):
        result = self.conn.execute(query)
        return list(result)

    # def add_messages(self, messages: List[Message]):
        