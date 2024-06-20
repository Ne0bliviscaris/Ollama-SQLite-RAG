from langchain_core.prompts import PromptTemplate


# Main, proven template for translating natural language questions into SQL queries - returns raw SQL query
def text_to_query():
    """You are a skilled data analyst. Generate a prompt template for translating natural language questions into SQL queries."""

    template = """
    **ROLE:** You are a skilled detective and data analyst. Given an input question, first create a syntactically correct {dialect} query to run, ensuring it retrieves all relevant records without imposing unnecessary limits. Then, look at the results of the query and return the answer. Use the following format:


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

    # Test 2 - good queries but hallucinated results
    # def text_to_query():
    # template = """
    # **Role:** You are a skilled database analyst. Your task is to translate natural language questions into syntactically correct {dialect} SQL queries, execute these queries to retrieve relevant records, and provide a concise and accurate answer based on the results.

    # **Input:**

    #     - **Question:** "Question here"
    #     - **SQLQuery:** "SQL Query to run"
    #     - **SQLResult:** "Result of the SQLQuery"
    #     - **Answer:** "Final answer here"

    #     **Only use the following tables:**

    #     {table_info}

    #     **Question:** {input}

    #     **TopK:** {top_k}
    #     """
    # prompt = PromptTemplate.from_template(template)
    # return prompt
