import sqlalchemy as db
from typing import List
from models.Message import Message
from dotenv import load_dotenv 
import os
from emoji_encodings import encodings
from utils import console_logger, ColorStatus

# init
load_dotenv()
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
schema_name = 'capstone'


class DataAccessObject:
    def __init__(self):
        # start db connection
        engine = db.create_engine(
            f"mysql+pymysql://{username}:{password}@{url}/{schema_name}", echo=False)

        self.conn = engine.connect()
    
    def get_messages(self):
        query = 'SELECT * FROM discord;'
        return list(self.conn.execute(query))
        
    def get_column_names(self):
        query = 'SHOW COLUMNS FROM discord;'
        return list(self.conn.execute(query))

    def add_messages(self, messages: List[Message]):
        # construct query string
        query = 'INSERT INTO discord (discord_id, joy, rofl, has_funny_emoji, content) VALUES '
        query_vals = list(self._get_query_vals(messages))

        # if no new data being added, exit function
        if not query_vals:
            console_logger("No new data to add.", status=ColorStatus.ERROR)
            return 

        # append query values
        query += ','.join(query_vals)

        # execute query
        # try:
        try:
            console_logger('Executing MySQL query...')
            self.conn.execute(query)
        except Exception as err:
            console_logger(err, status=ColorStatus.ERROR)
            return

        console_logger(f'\n***Messages successfully added {len(query_vals)} to DB****\n')


    def _is_saved_already(self, message: Message) -> bool:
            # makes DB call
            saved_messages = self.get_messages()

            # map message objects to their discord ID's
            saved_ids = [saved_message[0] for saved_message in saved_messages]
            return message.discord_id in saved_ids

    def _get_query_vals(self, messages: List[Message]):
        console_logger('Generating query values...')
        for iter, message in enumerate(messages):
            if message.discord_id == '897564089650405416':
                continue

            content = message.content
            # escape error-causing characters
            if content: 
                content = content.replace('\\', '')
                content = content.replace("'", "\\'")
                content = content.replace('"', '\\"')
                content = content.replace('%', '%%')
     
            # get message's joy and rofl counts
            discord_id = message.discord_id
            rofl = message.funny_emoji_counts.get(encodings['rofl'], 0)
            joy = message.funny_emoji_counts.get(encodings['joy'], 0)
            has_funny_emoji = message.has_funny_emojis

            yield f"({discord_id}, {joy}, {rofl}, {int(has_funny_emoji)}, '{content}')"
        




