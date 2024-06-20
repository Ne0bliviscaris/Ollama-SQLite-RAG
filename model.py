import time

from langchain.chains import create_sql_query_chain

import files.prompt_templates as templates
from connections import database_connect, get_db_schema, ollama_connect


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\nExecution time of {func.__name__}: {(end_time - start_time):.3f} seconds.")
        return result

    return wrapper


def build_langchain():
    """Builds and returns a language chain with database and Ollama connections."""
    db = database_connect()
    llm = ollama_connect(temperature=0)
    prompt = templates.text_to_query()
    chain = create_sql_query_chain(llm, db, prompt)
    return chain


@timer
def process_query_and_get_response(question):
    # Connect to the database and model, get table info
    chain = build_langchain()

    # Pass the question to the model
    table_info = get_db_schema()
    input_data = {"question": question, "table_info": table_info, "dialect": "sqlite", "top_k": 1}

    # Ask the question and get the response from the model
    response = chain.invoke(input_data)
    return response
