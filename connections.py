import sqlite3

from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import SQLDatabase

from files.settings import DB_FILE, MODEL, TEMPARATURE


def sql_query(query):
    """
    Connect to database and execute SQL query
    query: str - SQL query
    """
    db = DB_FILE  # database file
    connection = sqlite3.connect(db)  # connect to db
    cursor = connection.cursor()  # create cursor instance

    cursor.execute(f"{query}")  # execute query

    wyniki = cursor.fetchall()  # fetch all results
    for wiersz in wyniki:
        print(wiersz)  # print results

    connection.close()  # close connection


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


def ollama_connect(temperature=TEMPARATURE):
    """
    Establishes a connection to the Ollama model via Docker.

    Input:
        temperature: float - The temperature to use for the model.

    Returns:
        ChatOllama: An instance of the ChatOllama model with specified parameters.
    """
    llm = ChatOllama(model=MODEL, temperature=TEMPARATURE)
    return llm
