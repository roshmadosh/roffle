import pandas as pd


# passing dao an argument bc i don't know how to import things from modules "higher" in the project directory
def generate_csv(dao):
    messages = dao.get_messages()
    columns = dao.get_column_names()

    df = pd.DataFrame(messages, columns=columns)

    df.to_csv('./eda.csv')