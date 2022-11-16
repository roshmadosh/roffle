from dotenv import load_dotenv 
import os
from typing import List
from utils.color_console import console_logger, ColorStatus
from pyathena import connect


load_dotenv()

staging_dir = os.getenv('S3_STAGING_DIR')
athena_table = os.getenv('ATHENA_TABLE')


class AthenaAccessor:

    def __init__(self):
        self.cursor = connect(s3_staging_dir=staging_dir, region_name="us-east-1").cursor()
        self.table = athena_table
    
    def select_n(self, n):
        query_string = f"SELECT * FROM {athena_table} LIMIT 10"
        self.cursor.execute(query_string)
        # self.cursor.execute("""
        #        SELECT * FROM %(table)s
        #        LIMIT %(n)i
        #        """, { "table": athena_table, "n": n })

        query_result = self.cursor.fetchall()
        return query_result