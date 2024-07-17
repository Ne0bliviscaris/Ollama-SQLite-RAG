import modules.ai.model as model
from modules.ai.prompt_templates import conclude, text_to_query
from modules.database.db import sql_query


def launch_model(model_type, question):
    """Run the model and return the response."""
    model_response = model.model_response(model_type=model_type, question=question, temperature=0)
    return model_response


def sql_query(model_response):
    """Extract and run SQL query and return the result"""
    query = extract_query_from_model(model_response)
    query_result = sql_query(query)
    return query_result


def extract_query_from_model(model_response):
    """Get the query from the model response"""
    import re

    match = re.search(r"SELECT.*?(?:;|$)", model_response, re.IGNORECASE)
    if match:
        sql_query = match.group(0).strip()
        # Add a semicolon if missing
        if not sql_query.endswith(";"):
            sql_query += ";"
        return sql_query
    else:
        return "No SQL query found in the response."
