from time import time
import requests
from dotenv import load_dotenv 
import os
import json

# init
load_dotenv()   
url = "https://discord.com/api/v9/channels/1024420950076309526/messages"
auth = os.getenv("AUTH")
cookie = os.getenv("COOKIE")
output_file = os.getenv("OUTPUT_FILE")

def fetch_data():
    """
    Generates a txt file after fetching messages from Discord server. For preventing unnecessary API calls.
    """        
    # will contain messages to write to txt file
    messages = []

    # initial request for messages
    headers = {
        "Authorization": auth,
        "Cookie": cookie
    }
    raw_data = requests.get(url, headers=headers)
    json_data = raw_data.json()
    messages.extend(json_data)

    # discord sets a 50 message limit per request
    while len(json_data) == 50:
        # get oldest message in batch and append query param
        message_id = json_data[-1]['id']
        more_url = url + f'?before={message_id}'

        # complete request
        more_data = requests.get(more_url, headers=headers)
        json_data = more_data.json()
        messages.extend(json_data)

    # write to text file
    with open(output_file, 'w') as f:
        f.write(json.dumps(messages))

def get_data():
    # fetch from Discord server only if txt file not found
    if not os.path.exists(output_file):
        print('fetching data....')
        fetch_data()

    # return contents of file.
    with open(output_file) as f:
        line = f.readline()
        return json.loads(line)
