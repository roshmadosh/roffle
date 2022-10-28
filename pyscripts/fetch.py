from time import time
import requests
from dotenv import load_dotenv 
import os
import json
from datetime import datetime

load_dotenv()   
url = "https://discord.com/api/v9/channels/1024420950076309526/messages"
auth = os.getenv("AUTH")
cookie = os.getenv("COOKIE")

def fetch_data():

    headers = {
        "Authorization": auth,
        "Cookie": cookie
    }
    data_array = []
    raw_data = requests.get(url, headers=headers)
    json_data = raw_data.json()
    
    data_array.extend(json_data)

    # discord sets a 50 message limit per request
    while len(json_data) == 50:
        message_id = json_data[-1]['id']

        more_url = url + f'?before={message_id}'
        print('MORE URL', more_url)
        # request older messages and add to data_array
        more_data = requests.get(more_url, headers=headers)
        json_data = more_data.json()
        data_array.extend(json_data)

    
    with open('bds_data.txt', 'w') as f:
        f.write(json.dumps(data_array))

def get_data(filename: str):
    if not os.path.exists(filename):
        print('fetching data....')
        fetch_data()

    with open(filename) as f:
        line = f.readline()
        return json.loads(line)
