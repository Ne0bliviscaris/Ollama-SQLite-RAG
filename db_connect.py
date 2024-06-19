import sqlite3


def sql_query(query, limit=5):
    """
    Connect to database and execute SQL query
    query: str - SQL query
    limit: int - limit of results, default 5
    """
    db = "files/sql-murder-mystery.db"  # database file
    connection = sqlite3.connect(db)  # connect to db
    cursor = connection.cursor()  # create cursor instance

    cursor.execute(f"{query} LIMIT {limit}")  # execute query

    wyniki = cursor.fetchall()  # fetch all results
    for wiersz in wyniki:
        print(wiersz)  # print results

    connection.close()  # close connection
