from pyscripts.fetch import get_data
from db.DAO import DAO
from models.Message import Message

dao = DAO()

# Get data
raw_data = get_data()
messages = [Message(message_obj) for message_obj in raw_data]
print([(message.content, message.reactions) for message in messages])