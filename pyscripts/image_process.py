import json
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
import boto3
from utils import console_logger, ColorStatus

load_dotenv()

# --[CONSTANTS]-- #
BUCKETNAME = 'hiroshisawesometestbucket'
ROOT = os.getenv("ROOT")
FILENAME = f'{ROOT}/bds_data_list.txt'

# --[SETUP]-- #
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKETNAME)


# --[FUNCTIONS]-- #

def read_images_s3():
    images = []
    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()
        image_obj =  { "id": key, "PIL_Image": body}

        # Code for showing images from byte data saved in S3
        # img = Image.open(BytesIO(body))
        # img.show()
        images.append(image_obj)
    
    return images

def save_images_s3():
    # filter out objects already saved to s3
    txt_contents = get_txt_urls()
    txt_ids = [img['id'] for img in txt_contents]

    console_logger(f'Reading S3 bucket for existing images...')
    s3_contents = read_images_s3()
    s3_ids = [content['id'] for content in s3_contents]

    console_logger("Filtering out saved images...")
    filtered_ids = set(txt_ids).difference(set(s3_ids))
    filtered_content = [content for content in txt_contents if content['id'] in filtered_ids]

    # perform requests for images from Discord and save them to S3
    for content in filtered_content:
        id = content['id']
        console_logger(f"FETCH: image with ID: {id}")
        response_body = requests.get(content['url'])
        response = { 'id': id, 'content': response_body.content }
        console_logger(f"SAVE: image with ID: {id}")
        s3.Bucket(BUCKETNAME).put_object(Key=response['id'], Body=BytesIO(response['content'])) 
        
    console_logger(f"Images saved to S3. Total of {len(filtered_content)} saved", ColorStatus.SUCCESS)

def get_txt_urls():
    # read from txt file containing raw data for messages
    messages = []
    with open(FILENAME) as f:
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


# for testing functions from terminal
if __name__ == '__main__':
    read_images_s3()