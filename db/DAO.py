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
    
    def get_messages(self):
        query = 'SELECT * FROM discord;'
        return list(self.conn.execute(query))

    #TODO Filter out messages that have already been saved
    def add_messages(self, messages: List[Message]):
        # construct query string
        query = 'INSERT INTO discord (discord_id, joy, rofl, content) VALUES '
        query_vals = list(self._get_query_vals(messages))

        # if no new data being added, exit function
        if not query_vals:
            print("No new data to add.")
            return 

        # append query values
        query += ','.join(query_vals)

        # execute query
        self.conn.execute(query)
        print(f'\n***Messages successfully added {len(query_vals)} to DB****\n')


    def _is_saved_already(self, message: Message) -> bool:
            # makes DB call
            saved_messages = self.get_messages()

            # map message objects to their discord ID's
            saved_ids = [saved_message[0] for saved_message in saved_messages]
            return message.discord_id in saved_ids

    def _get_query_vals(self, messages: List[Message]):
        for message in messages:
            # filter out messages without laughing emojis
            if not message.has_funny_emojis:
                continue
            
            # filter messages already saved to DB
            if self._is_saved_already(message):
                continue

            content = message.content
            # escape single and double quotes 
            if content: 
                content = content.replace("'", "\\'")
                content = content.replace('"', '\\"')

            # get message's joy and rofl counts
            discord_id = message.discord_id
            rofl = message.funny_emoji_counts.get(encodings['rofl'], 0)
            joy = message.funny_emoji_counts.get(encodings['joy'], 0)

            yield f"({discord_id}, {joy}, {rofl}, '{content}')"
        




