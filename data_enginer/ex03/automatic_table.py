import pandas as pd
import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

def load_csv_to_dataframe_from_folder(path_folder):
    dict_dataframe = {}
    for file in os.listdir(path_folder):
        if file.endswith('.csv'):
            dict_dataframe[file[:-4]] = pd.read_csv(path_folder + "/" + file)
    return dict_dataframe

def table_exists(engine, table_name):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if table_name in metadata.tables:
        print(f"Table {table_name} already exists")
    return table_name in metadata.tables
    
def create_schema_table_from_dataframe(dataframe, table_name, engine):
    metadata = MetaData()
    table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        *(Column(column, String, nullable=True) for column in dataframe.columns)
    )
    if not table_exists(engine, table_name):
        metadata.create_all(engine)
        print(f"Table {table_name} created")
    return table

def insert_dataframe_to_table(dataframe, table, engine):
    with engine.connect() as connection:
        dataframe.to_sql(name=table.name, con=connection, if_exists='append', index=False)
        print(f"Data inserted into table {table.name}")

def main():
    dataframes_dict = load_csv_to_dataframe_from_folder("../subject/customer")

    DB_NAME = 'piscineds'
    DB_USER = 'jgautier'
    DB_PASSWORD = 'mysecretpassword'
    DB_HOST = 'localhost'
    DB_PORT = '5432'

    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    engine = create_engine(DATABASE_URL)
        
    for table_name, dataframe in dataframes_dict.items():
        table = create_schema_table_from_dataframe(dataframe, table_name, engine)
        insert_dataframe_to_table(dataframe, table, engine)

if __name__ == "__main__":
    main()