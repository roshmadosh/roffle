from db import DataAccessObject
import pandas as pd


dao = DataAccessObject()
messages = dao.get_messages()
columns_raw = dao.get_column_names()
columns = [col[0] for col in columns_raw]
print(columns)

df = pd.DataFrame(messages, columns=columns)
print(df)