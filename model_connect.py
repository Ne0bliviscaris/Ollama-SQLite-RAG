import time

from langchain.chains import create_sql_query_chain
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate

import db_connect
from files.settings import DB_FILE, MODEL  # , MODEL_URL - switched to local model


def chain_connect():
    # Build the chain and prompt template
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")
    # Ollama model connection via Docker
    llm = ChatOllama(model=MODEL, temperature=0.01)

    return db, llm


def get_db_schema():
    """
    Get the schema of the database

    Returns:
    schema: dict - schema of the database"""
    schema = db_connect.get_schema()
    return schema


def query_translation_prompt_template():
    """Generates a prompt template for translating natural language questions into SQL queries."""

    template = """Given an input question, first create a syntactically correct {dialect} query to run, ensuring it retrieves all relevant records without imposing unnecessary limits. Then, look at the results of the query and return the answer. Use the following format:


    **Input:**

    - **Question:** "Question here"
    - **SQLQuery:** "SQL Query to run"
    - **SQLResult:** "Result of the SQLQuery"
    - **Answer:** "Final answer here"

    **Only use the following tables:**

    {table_info}

    **Question:** {input}

    **TopK:** {top_k}
    """
    prompt = PromptTemplate.from_template(template)
    return prompt


def prompt(question):
    start_time = time.time()  # Rozpoczęcie pomiaru czasu

    # Connect to the database and model, get table info
    db, llm = chain_connect()
    prompt = query_translation_prompt_template()

    chain = create_sql_query_chain(llm, db, prompt)

    # Compressed question v3
    table_info = get_db_schema()
    input_data = {"question": question, "table_info": table_info, "dialect": "sqlite", "top_k": 1}

    # Ask the question and get the response from the model
    response = chain.invoke(input_data)

    end_time = time.time()  # Zakończenie pomiaru czasu
    print(f"Czas wykonania: {end_time - start_time} sekund.")  # Wyświetlenie czasu wykonania

    return response
