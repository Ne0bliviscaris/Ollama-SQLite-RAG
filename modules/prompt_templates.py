from langchain_core.prompts import PromptTemplate


# backup main prompt
def text_to_query():
    """Prompt template to translate text instructions into SQL query"""

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
    prompt_template = PromptTemplate.from_template(template)
    return prompt_template


#  Working template
# def interpret_query():
#     """Prompt template to interpret SQL query results and provide a final answer."""

#     template = """
#     **ROLE:** You are a skilled detective. You are trying to solve a murder case and search for clues. You received results to analyze. Interpret the results and provide a very concise, focused answer. Then formulate next step instruction in a way, that can be forwarded to text-to-SQL model to progress the investigation. Give clear, concise instruction for the model. You do not write SQL query personally. If you find multiple clues, separate suggestions for each of them.

#     **Input:**

#     - **Input:** "These are the received results you have to interpret"
#     - **Answer:** "Concise answer here. Analyze how SQLResult searching for clues."
#     - **Next step:** Concise guidance how to proceed the investigation
#     - **Model instruction:** Clear instructions for the text-to-sql translation model to proceed the investigation. Do not use any references. Give one instruction at a time. If you have more, list them.

#     **Only use the following tables:**

#     {table_info}

#     **Input:** {input}

#     **TopK:** {top_k}
#     """
#     prompt_template = PromptTemplate.from_template(template)
#     return prompt_template


#  Test template
def conclude():
    """Prompt template to interpret SQL query results and provide a final answer."""

    template = """
    **ROLE:** You are a skilled detective. You are trying to solve a murder case and search for clues. Analyze received information. Interpret the results and provide a very concise, focused conclusion. Do not use any spare words. 


    **Input:**

    - **Input:** "These are the received results you have to interpret"

    Only write a short, concise conclusion.

    - **Answer:** "Concise conclusion here."

    **Only use the following tables:**

    {table_info}

    **Input:** {input}

    **TopK:** {top_k}
    """
    prompt_template = PromptTemplate.from_template(template)
    return prompt_template
