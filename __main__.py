from db import DataAccessObject, S3Accessor, FileIO
from models.Message import Message
from pyscripts.generate_eda import generate_csv
from pyscripts.discord import discord_fetch
import os
from dotenv import load_dotenv

load_dotenv()

fileIO = FileIO('bds_data')
messages = fileIO.read_files()
s3 = S3Accessor(os.getenv('BUCKETNAME'))
s3.save_images_s3()






