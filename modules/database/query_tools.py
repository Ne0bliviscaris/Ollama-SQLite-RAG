import re


def sql_regex() -> str:
    """Define regex pattern components for SQL query."""
    SELECT = r"SELECT"
    anything = r".*?"  # Non-greedy match of any text
    FROM = r"FROM"
    QUERY_END = r"(?=\n|$)"  # End of line or string

    return f"({SELECT} {anything} {FROM} {anything}){QUERY_END}"


def extract_sql_query(model_response: str) -> str:
    """Extract SQL SELECT query with FROM clause from the response string."""
    regex = sql_regex()
    # Search for SQL query with case-insensitive flag
    match = re.search(regex, model_response, re.IGNORECASE | re.DOTALL)

    if match:
        sql_query = match.group(1).strip()
        return sql_query

    return "No valid SQL query found in the response."
