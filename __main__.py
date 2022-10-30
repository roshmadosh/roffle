from pyscripts.fetch import get_data
from db.DAO import DAO
from models.Message import Message

dao = DAO()

# Get data
raw_data = get_data()

# convert to list of Message objects
messages = [Message(message_obj) for message_obj in raw_data]

# make db call
dao.add_messages(messages)