from langchain.chains import create_sql_query_chain
from langchain_community.llms.ollama import Ollama
from langchain_community.utilities import SQLDatabase

from files.settings import DB_FILE, MODEL, MODEL_URL


def prompt(prompt):
    """
    Prompt a selected model.
    """
    # Database connection
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")

    # Ollama model connection via Docker
    llm = Ollama(model=MODEL, base_url=MODEL_URL, temperature=0)
    chain = create_sql_query_chain(llm, db)

    # Static instructions for the model
    STATIC_MESSAGE = "You are an experienced data scientist. Answer only with SQL query to prove it. Make the query one line. Use the simplest and most efficient query"

    # Generate response
    response = chain.invoke({"question": f"{prompt} {STATIC_MESSAGE}"})
    print(response)
