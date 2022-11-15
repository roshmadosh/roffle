from PIL import Image
import requests
from io import BytesIO
import boto3
from utils.color_console import console_logger, ColorStatus
from typing import List
from db import FileIO

class S3Accessor:
    def __init__(self, bucket_name: str) -> None:
        s3 = boto3.resource('s3')

        # bucket "cursor"
        self.bucket = s3.Bucket(bucket_name)
    
    def read_images(self) -> List:
        images = []
        for obj in self.bucket.objects.all():
            console_logger(f'Reading {obj.key} from S3...')
            key = obj.key
            body = obj.get()['Body'].read()
            image_obj =  { "id": key, "PIL_Image": body}

            # Code for showing images from byte data saved in S3
            # img = Image.open(BytesIO(body))
            # img.show()
            images.append(image_obj)
    
        console_logger('Successfully read all images from S3!', status=ColorStatus.SUCCESS)
        return images

    def save_images_s3(self):
        # filter out objects already saved to s3
        filereader = FileIO('bds_data')
        
        txt_contents = filereader.get_img_urls()
        txt_ids = [img['id'] for img in txt_contents]

        console_logger(f'Reading S3 bucket for existing images...')
        s3_contents = self.read_images()
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
            self.bucket.put_object(Key=response['id'], Body=BytesIO(response['content'])) 
            
        console_logger(f"Images saved to S3. Total of {len(filtered_content)} saved", ColorStatus.SUCCESS)

