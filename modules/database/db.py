import sqlite3

from langchain_community.utilities import SQLDatabase

from modules.settings import DB_FILE
from modules.tools import convert_list_to_string


def execute_sql_query(extracted_query):
    """Connect to database and execute SQL query"""
    with sqlite3.connect(DB_FILE) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(extracted_query)
        results = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        results_str = convert_list_to_string(results, column_names)
        return results_str


def get_db_schema():
    db = db_without_solution()
    return db.get_table_info()


def database_connect():
    """Establishes a connection to the SQL database using the provided URI."""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")
    return db


def db_without_solution():
    """Connects to SQL database. Solution table is excluded."""
    return SQLDatabase.from_uri(f"sqlite:///{DB_FILE}", ignore_tables=["solution"])
