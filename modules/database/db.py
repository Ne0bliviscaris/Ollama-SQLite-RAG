import sqlite3

from langchain_community.utilities import SQLDatabase

from modules.database.tools import convert_list_to_string
from modules.settings import DB_FILE


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
    """Get filtered database schema showing only table structures."""
    with sqlite3.connect(DB_FILE) as connection:  # Use direct sqlite3 connection
        cursor = connection.cursor()
        banned_tables = ["solution"]

        schema_parts = []

        # Get all table names excluding banned ones
        cursor.execute(
            """
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            AND name NOT IN ('sqlite_sequence')
            AND name NOT IN (?);
        """,
            (",".join(banned_tables),),
        )

        tables = cursor.fetchall()

        for (table_name,) in tables:
            # Get only CREATE TABLE statement
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            create_statement = cursor.fetchone()[0]
            # Clean up the statement and add to schema
            clean_statement = create_statement.replace("\n", " ").strip()
            schema_parts.append(clean_statement)

    return "\n\n".join(schema_parts)


def database_connect():
    """Establishes a connection to the SQL database using the provided URI."""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")
    return db


def db_without_solution():
    """Connects to SQL database. Solution table is excluded."""
    return SQLDatabase.from_uri(f"sqlite:///{DB_FILE}", ignore_tables=["solution"])
