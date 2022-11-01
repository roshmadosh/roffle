import sqlalchemy as db
from typing import List
from models.Message import Message
from dotenv import load_dotenv 
import os
from emoji_encodings import encodings


# init
load_dotenv()
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
schema_name = 'capstone'


class DAO:
    def __init__(self):
        # start db connection
        engine = db.create_engine(
            f"mysql+pymysql://{username}:{password}@{url}/{schema_name}", echo=False)

        self.conn = engine.connect()


    def add_messages(self, messages: List[Message]):
        # construct query string
        query = 'INSERT INTO discord (joy, rofl, content) VALUES '
        query_vals = list(self._get_query_vals(messages))
        query += ','.join(query_vals)

        # execute query
        self.conn.execute(query)
        print(f'\n***Messages successfully added {len(query_vals)} to DB****\n')
   
    def _get_query_vals(self, messages: List[Message]):
        for message in messages:

            # filter funny messages
            if not message.has_funny_emojis:
                continue
            
            content = message.content
            # escape single and double quotes 
            if content: 
                content = content.replace("'", "\\'")
                content = content.replace('"', '\\"')

            # get message's joy and rofl counts
            rofl = message.funny_emoji_counts.get(encodings['rofl'], 0)
            joy = message.funny_emoji_counts.get(encodings['joy'], 0)

            yield f"({joy}, {rofl}, '{content}')"