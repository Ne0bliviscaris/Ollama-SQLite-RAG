import re


def extract_query_from_string(model_response):
    """Get the query from the model response"""

    match = re.search(r"SELECT.*?(?:;|$)", model_response, re.IGNORECASE)
    if match:
        sql_query = match.group(0).strip()
        # Add a semicolon if missing
        if not sql_query.endswith(";"):
            sql_query += ";"
        return sql_query
    else:
        return "No SQL query found in the response."


def convert_query_result_to_string(results):
    """
    Convert query results to a string, each row from a new line."""
    results_string = "\n".join([str(row) for row in results])
    return results_string
