from pyscripts.fetch import get_data
from db.DataAccessObject import DataAccessObject
from models.Message import Message
from pyscripts.image_process import save_images_s3

dao = DataAccessObject()

# Get data without filtering funny messages
raw_data = get_data()

# convert each item in raw data to a Message object
messages = [Message(message_obj) for message_obj in raw_data]

# make db call
dao.add_messages(messages)

# save images to S3
# save_images_s3()
