import requests
import os
from dotenv import load_dotenv 
from utils.color_console import console_logger
from typing import List

load_dotenv()   

# a URL for each channel in the server
urls =[
    "https://discord.com/api/v9/channels/1024420950076309526/messages",
    "https://discord.com/api/v9/channels/1024716900485320754/messages",
    "https://discord.com/api/v9/channels/1027998668843917374/messages",
    "https://discord.com/api/v9/channels/869309676418891789/messages", # REVATURE, channel: general
    "https://discord.com/api/v9/channels/899658406422523904/messages", # REVATURE, channel: hibachi-grilling
]

auth = os.getenv("AUTH")
cookie = os.getenv("COOKIE")


def discord_fetch() -> List:
    """
    Generates a txt file after fetching messages from Discord server. For preventing unnecessary API calls.
    """        
    # will contain messages to write to txt file
    messages = []
    headers = {
        "Authorization": auth,
        "Cookie": cookie
    }

    # initial request for messages
    for url in urls:
        console_logger(f'Fetching data from {url}')
        raw_data = requests.get(url, headers=headers)
        json_data = raw_data.json()
        messages.extend(json_data)

        # discord sets a 50 message limit per request
        i = 1
        while len(json_data) == 50:
            console_logger(f'Fetching page {i} from {url}')
            # get oldest message in batch and append query param
            message_id = json_data[-1]['id']
            more_url = url + f'?before={message_id}'

            # complete request
            more_data = requests.get(more_url, headers=headers)
            json_data = more_data.json()
            messages.extend(json_data)
            i += 1
    return messages


    