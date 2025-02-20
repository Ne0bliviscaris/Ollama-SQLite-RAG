from langchain.chains import create_sql_query_chain
from langchain_community.chat_models import ChatOllama

from modules.ai.prompt_templates import conclude, text_to_query
from modules.database.db import database_connect, get_db_schema
from modules.settings import MODEL, MODEL_TIMEOUT


def build_langchain(template, temperature=0):
    """Builds and returns a language chain with database and Ollama connections."""
    db = database_connect()
    llm = ollama_connect(temperature=temperature)
    chain = create_sql_query_chain(llm, db, template)
    return chain


def select_prompt_template(model_type):
    if model_type == "SQL Translator":
        return text_to_query()
    elif model_type == "Detective":
        return conclude()


def model_response(model_type, question, temperature=0):
    """Launch the model and return the response."""
    try:
        # Connect to the database and model, get table info
        template = select_prompt_template(model_type)
        chain = build_langchain(template, temperature)

        # Pass the question to the model
        table_info = get_db_schema()
        input_data = {"question": question, "table_info": table_info, "dialect": "sqlite", "top_k": 1}

        # Ask the question and get the response from the model

        response = chain.invoke(input_data)
        return response
    except Exception as e:
        return f"Model Connection error. Make sure Ollama is running and {MODEL} is installed."


def ollama_connect(temperature=0):
    """Establishes a connection to the Ollama model via Docker.
    temperature: float - model creativity parameter."""
    llm = ChatOllama(model=MODEL, temperature=temperature, request_timeout=MODEL_TIMEOUT)
    return llm


def split_model_answer(model_answer: str) -> tuple[str, str]:
    """Split model output into thinking process and final answer."""
    # Szukamy znaczników <think> i </think>
    THINK_START = "<think>"
    content = "(.*?)"
    THINK_END = "</think>"
    think_pattern = rf"{THINK_START}{content}{THINK_END}"
    import re

    thinking = re.search(think_pattern, model_answer, re.DOTALL)
    thinking_process = thinking.group(1).strip() if thinking else ""

    output = re.sub(pattern=think_pattern, repl="", string=model_answer, flags=re.DOTALL).strip()

    return output, thinking_process
