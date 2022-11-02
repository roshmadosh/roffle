import requests
from dotenv import load_dotenv 
import os
import json


load_dotenv()   

# a URL for each channel in the server
urls =[
    "https://discord.com/api/v9/channels/1024420950076309526/messages",
    "https://discord.com/api/v9/channels/1024716900485320754/messages",
    "https://discord.com/api/v9/channels/1027998668843917374/messages"
]
auth = os.getenv("AUTH")
cookie = os.getenv("COOKIE")
output_file = "bds_data.txt"
output_file_list = "bds_data_list.txt"

def get_data():
    # fetch from Discord server only if txt file not found
    if not os.path.exists(output_file) or not os.path.exists(output_file_list):
        print('fetching data....')
        discord_fetch()

    # return contents of file.
    with open(output_file) as f:
        messages = []
        for message in f:
            messages.append(json.loads(message))

        return messages

def discord_fetch():
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
            for message in messages:
                f.write(json.dumps(message))
                f.write("\n")
        with open(output_file_list, 'w') as f:
            f.write(json.dumps(messages))

    