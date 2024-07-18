import re
import sqlite3

from langchain_community.utilities import SQLDatabase

from modules.settings import DB_FILE


def execute_sql_query(extracted_query):
    """
    Connect to database and execute SQL query
    query: str - SQL query

    Returns:
        results_string: str - Results of the query as a string
    """
    db = DB_FILE  # database file
    with sqlite3.connect(db) as db_connection:  # connect to db using context manager
        cursor = db_connection.cursor()  # create cursor instance
        cursor.execute(extracted_query)  # execute query
        results = cursor.fetchall()  # each row is a tuple, all rows are in a list

    return results  # connection is automatically closed


def get_db_schema():
    """
    Get the schema of the database

    Returns:
    schema: dict - schema of the database"""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")

    schema = db.get_table_info()
    return schema


def database_connect():
    """
    Establishes a connection to the SQL database using the provided URI.

    Returns:
        SQLDatabase: An instance of the SQLDatabase connected to the specified database.
    """
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")
    return db
