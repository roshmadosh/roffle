from db import DataAccessObject, S3Accessor, FileIO
from pyscripts.generate_eda import generate_csv
import os
from dotenv import load_dotenv


load_dotenv()


fileIO = FileIO('bds_data')

s3 = S3Accessor(os.getenv('BUCKETNAME'))

image = s3.read_image_by_key('1000048112674537613')


image.display_image()






