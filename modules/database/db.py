import sqlite3

from langchain_community.utilities import SQLDatabase

from modules.settings import DB_FILE


def execute_sql_query(extracted_query):
    """Connect to database and execute SQL query"""
    db = DB_FILE
    with sqlite3.connect(db) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(extracted_query)
        results = cursor.fetchall()

    return results


def get_db_schema():
    """Get the schema of the database"""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")

    schema = db.get_table_info()
    return schema


def database_connect():
    """Establishes a connection to the SQL database using the provided URI."""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")
    return db
