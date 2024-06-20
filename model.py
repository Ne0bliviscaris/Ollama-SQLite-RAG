import time

from langchain.chains import create_sql_query_chain

import files.prompt_templates as templates
from connections import database_connect, get_db_schema, ollama_connect


def build_langchain():
    """Builds and returns a language chain with database and Ollama connections."""
    db = database_connect()
    llm = ollama_connect()
    prompt = templates.query_translation()
    chain = create_sql_query_chain(llm, db, prompt)
    return chain


def process_query_and_get_response(question):
    start_time = time.time()  # Rozpoczęcie pomiaru czasu

    # Connect to the database and model, get table info
    chain = build_langchain()

    # Compressed question v3
    table_info = get_db_schema()
    input_data = {"question": question, "table_info": table_info, "dialect": "sqlite", "top_k": 1}

    # Ask the question and get the response from the model
    response = chain.invoke(input_data)

    end_time = time.time()  # Zakończenie pomiaru czasu
    print(f"Czas wykonania: {end_time - start_time} sekund.")  # Wyświetlenie czasu wykonania

    return response
