from dataclasses import replace
import sqlalchemy as db
from typing import List
from models.Message import Message
from dotenv import load_dotenv 
import os
from emoji_encodings import encodings, replacements


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


    def add_messages(self, messages: List[Message]):
        query = 'INSERT INTO discord (joy, rofl, content) VALUES '
        query_vals = list(self._get_query_vals(messages))
        query += ','.join(query_vals)

      
        print(query)
        self.conn.execute(query)
   
    def _get_query_vals(self, messages: List[Message]):
        for message in messages:
            if not message.has_funny_emojis:
                continue
            
            content = message.content
            if content: 
                content = content.replace("'", "\\'")
                content = content.replace('"', '\\"')

            rofl = message.funny_emoji_counts.get(encodings['rofl'], 0)
            joy = message.funny_emoji_counts.get(encodings['joy'], 0)

            yield f"({joy}, {rofl}, '{content}')"