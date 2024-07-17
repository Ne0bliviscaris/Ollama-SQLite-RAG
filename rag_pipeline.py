import modules.ai.model as model
import modules.db as db
from modules.ai.prompt_templates import conclude, text_to_query


def launch_model(model_type, question, template, prints=False):
    """Run the model and return the response."""
    model_response = model.model_response(model_type, question=question, template=template, temperature=0)

    # Print the user input and model response on demand
    if prints == True:
        print(f"\nModel type: \n{model_type}")
        print(f"\nModel answer:\n{model_response}")
    return model_response


def sql_query(model_response, prints=False):
    """Run SQL query and return the result"""

    if prints == True:
        print(f"Forwarding SQL Query")

    query_result = db.sql_query(model_response)

    # Print the SQL query result on demand
    if prints == True:
        print(f"\nSQL Query Result:\n{query_result}")
    return query_result


def rag(question, prints=False):
    """Full pipeline to answer a database related question using RAG model."""

    # Step 1: Translate text instructions into SQL query
    model_response = launch_model("SQL Translator", question, text_to_query(), prints)

    # Step 2: Run SQL query and return the result
    query_results = sql_query(model_response, prints)

    # Step 3: Interpret SQL query results and provide a final answer
    rag_answer = launch_model("Detective", query_results, conclude(), prints)

    # Print the RAG answer unconditionally
    return rag_answer


if __name__ == "__main__":
    question = """
    Extract police MURDER type crime scene reports from 'SQL City' at 15 january 2018
    """
    # question = """
    # The  witness resides at the last house on "Northwestern Dr"
    # """
    # question = """
    # find who lives in 'Northwestern Dr', 4919
    # """
    # question = """
    # find out more about Christopher Peteuil with license ID 993845
    # """
    rag(question, True)
