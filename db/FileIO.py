from typing import List
import json
import os
from dotenv import load_dotenv
from utils.color_console import console_logger, ColorStatus
from models import Message

load_dotenv()


class FileIO:
    def __init__(self, filename: str):
        root = os.getenv("ROOT")
        self.filename = f'{root}/{filename}.txt'
        self.filename_list = f'{root}/{filename}_list.txt'

    def get_img_urls(self) -> List:
        # read from txt file containing raw data for messages
        messages = []
        with open(self.filename_list) as f:
            message = f.read()
            messages.extend(json.loads(message))

        # get urls from each message JSON
        img_urls = []
        for message in messages: 
            attachment = message.get('attachments', '')
            url = attachment[0].get('url', '') if attachment else ''

            if url:
                message_obj = { "id": message['id'], "url": url }
                img_urls.append(message_obj) 

        return img_urls
    
    def read_filename(self) -> List[Message]:
        # fetch from Discord server only if txt file not found
        if not os.path.exists(self.filename) or not os.path.exists(self.filename_list):
            raise FileNotFoundError()

        
        # return contents of file.
        with open(self.filename) as f:
            messages = []
            for message in f:
                messages.append(json.loads(message))

        return [Message(message) for message in messages]
    
    def read_filename_by_id(self, discord_id: str) -> Message:
        messages = self.read_filename()
        filter_result = [message for message in messages if message.discord_id == discord_id]
        if filter_result:
            return filter_result
        else:
            raise ValueError(f'{discord_id} not found in {self.filename}')

    def write_files(self, messages):
        if os.path.exists(self.filename):
            raise FileExistsError(f'{self.filename} already exists')

        # write to text file
        with open(self.filename, 'w') as f:
            console_logger(f'Writing to {self.filename}')
            for message in messages:
                f.write(json.dumps(message))
                f.write("\n")
                
        with open(self.filename_list, 'w') as f:
            console_logger(f'Writing to {self.filename_list}')
            f.write(json.dumps(messages))