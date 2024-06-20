import sqlite3

from langchain_community.utilities import SQLDatabase

from files.settings import DB_FILE


def sql_query(query="Select * from PEOPLE", limit=5):
    """
    Connect to database and execute SQL query
    query: str - SQL query
    limit: int - limit of results, default 5
    """
    db = DB_FILE  # database file
    connection = sqlite3.connect(db)  # connect to db
    cursor = connection.cursor()  # create cursor instance

    cursor.execute(f"{query} LIMIT {limit}")  # execute query

    wyniki = cursor.fetchall()  # fetch all results
    for wiersz in wyniki:
        print(wiersz)  # print results

    connection.close()  # close connection


def get_schema():
    # Database connection
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")

    schema = db.get_table_info()
    return schema
