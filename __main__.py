from pyscripts.fetch import get_data
import sqlalchemy as db
from dotenv import load_dotenv 
import os

# Get data
filename = 'bds_data.txt'
bds = get_data(filename)

# Save to DB
load_dotenv()
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
schema_name = 'capstone'

engine = db.create_engine(
    f"mysql+pymysql://{username}:{password}@{url}/{schema_name}", echo=False)

conn = engine.connect()

result = conn.execute("SELECT * FROM discord")

print('RESULT:', list(result))