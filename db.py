import sqlite3

from langchain_community.utilities import SQLDatabase

from files.settings import DB_FILE


def sql_query(query):
    """
    Connect to database and execute SQL query
    query: str - SQL query

    Returns:
        results_string: str - Results of the query as a string
    """
    db = DB_FILE  # database file
    connection = sqlite3.connect(db)  # connect to db
    cursor = connection.cursor()  # create cursor instance

    cursor.execute(f"{query}")  # execute query

    results = cursor.fetchall()  # fetch all results
    results_string = query_result_to_string(results)

    connection.close()  # close connection
    return results_string


def query_result_to_string(results):
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
