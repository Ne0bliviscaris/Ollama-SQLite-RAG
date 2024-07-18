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


def extract_query_from_string(model_response):
    """Get the query from the model response"""

    match = re.search(r"SELECT.*?(?:;|$)", model_response, re.IGNORECASE)
    if match:
        sql_query = match.group(0).strip()
        # Add a semicolon if missing
        if not sql_query.endswith(";"):
            sql_query += ";"
        return sql_query
    else:
        return "No SQL query found in the response."


def convert_query_result_to_string(results):
    """
    Convert query results to a string, each row from a new line.
    results: list of tuples - The result from a SQL query execution.
    """
    results_string = "\n".join([str(row) for row in results])
    return results_string


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
