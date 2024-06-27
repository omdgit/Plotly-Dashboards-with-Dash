"""
Created on Sat Aug 6, 2022

@author: omd
First Version: 08.06.2022

This module includes some custom functions to read from and write to some databases:
 - SQLite
 - POSTGRES
"""
# from gettext import npgettext
from sqlalchemy import create_engine
import pandas as pd
import sqlite3
from sqlite3 import Error

__version__ = '8.6.2022'

def from_sqlite(sql: str, database: str)-> pd.DataFrame:
    """This function pulls data from a SQLite database and returns a dataframe object

    Args:
        sql (str): This SQL statement determines which data is pulled
        database (str): The name of the database from which to pull the data
    """
    engine = create_engine('sqlite:///' + database)
    return pd.read_sql(sql, engine)


def to_sqlite(dataframe: pd.DataFrame, dataframe_name: str, database: str):
    """This function creates a table in selected database and writes data from dataframe to the new table.

    Args:
        dataframe (pd.DataFrame): The dataframe that is saved as a table
        dataframe_name (str): The name of the new database table
        database (str): The name of the database where to create the table. Include path if different from
                        current location (e.g. database = "/Users/johnsmith/Documents/datasets.db")
    """
    engine = create_engine('sqlite:///' + database)
    dataframe.to_sql(dataframe_name, engine, index=False, if_exists="replace")


def from_postgres(sql: str, database: str)-> pd.DataFrame:
    """This function pulls data from a POSTGRES database and returns a dataframe object

    Args:
        sql (str): This SQL statement determines which data is pulled
        database (str): The name of the database from which to pull the data
    """
    engine = create_engine('postgresql://postgres:Leaves@localhost:5432/' + database)
    return pd.read_sql(sql, engine)


def to_postgres(dataframe: pd.DataFrame, dataframe_name:str, database: str):
    """This function creates a table in selected database and writes data from dataframe to the new table.

    Args:
        dataframe (pd.DataFrame): The dataframe that is saved as a table
        dataframe_name (str): The name of the new database table
        database (str): The name of the database where to create the table
    """
    engine = create_engine('postgresql://postgres:Leaves@localhost:5432/' + database)
    dataframe.to_sql(dataframe_name, engine, index=False)


def drop_table_sqlite(table: str, database: str):
    """This function let's you drop a table of a sqlite database.

    Args:
        table (str): the table/view to be dropped
        database (str): the database where the table/view is stored
    """
    from sqlalchemy import MetaData, Table
    # Create an engine to connect to the database
    engine = create_engine(f'sqlite:///{database}')

    # Create a metadata object to reflect the database schema
    metadata = MetaData(bind=engine) #, reflect=True)

    # Get the table object for the table you want to delete
    my_table = Table(table, metadata, autoload=True)

    # Use the drop() method to delete the table
    my_table.drop()

def create_connection(db_file):
    """Create a sqlite database

    Args:
        db_file (_type_): the database name
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn: 
            conn.close()
