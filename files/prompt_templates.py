from langchain_core.prompts import PromptTemplate


def query_translation():
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
