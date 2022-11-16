from db import DataAccessObject, S3Accessor, FileIO, AthenaAccessor
from pyscripts.generate_eda import generate_csv
import os
from dotenv import load_dotenv


load_dotenv()


# fileIO = FileIO('bds_data')

# s3 = S3Accessor('athena-bucket-for-roffle')

# s3.save_json('bds_data.txt')

athena = AthenaAccessor()

contents = athena.select_n(10)





