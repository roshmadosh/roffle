import requests
import boto3
from utils.color_console import console_logger, ColorStatus
from typing import List
from db import FileIO
from models import S3_Image
from io import BytesIO
import json


class S3Accessor:
    def __init__(self, bucket_name: str) -> None:
        s3 = boto3.resource('s3')

        # bucket "cursor"
        self.bucket = s3.Bucket(bucket_name)
    
    def read_images(self) -> List[S3_Image]:
        images = []
        for obj in self.bucket.objects.all():
            console_logger(f'Reading {obj.key} from S3...')
            img = S3_Image(key=obj.key, body=obj.get()['Body'].read())
            images.append(img)
    
        console_logger('Successfully read all images from S3!', status=ColorStatus.SUCCESS)
        return images

    def read_image_by_key(self, discord_id:str) -> S3_Image:
        images = self.bucket.objects.all()

        # converting to S3_Image objects in for-loop bc I can't get image body otherwise
        # for obj in images:
        #     console_logger(obj.get())
        #     console_logger(f'Converting {obj.key} to S3_Image object...')
        #     s3_images.append(S3_Image(obj.key, obj.get()['Body'].read()))

        filter_result = [s3_image for s3_image in images if s3_image.key == discord_id]
        
        if not filter_result :
            raise FileNotFoundError(f'{discord_id} not found in S3 bucket.')

        s3_image = S3_Image(filter_result[0].key, filter_result[0].get()['Body'].read())
        
        return s3_image


    def save_images(self):
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

    def save_json(self, filename):
        with open(filename, 'rb') as file:
            self.bucket.put_object(Key=filename, Body=file)
