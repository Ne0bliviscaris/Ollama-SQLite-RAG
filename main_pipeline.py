import db
import modules.model as model
from modules.prompt_templates import interpret_query, text_to_query


def step1_text_to_sql(question, prints=False):
    """Step 1: Translate text instructions into SQL query"""
    model_response = model.model_response(question=question, template=text_to_query(), temperature=0)
    if prints == True:
        print(f"\nQuestion: \n{question}")
        print(f"Model answer:\n{model_response}")
    return model_response


def step2_sql_query(model_response, prints=False):
    """Step 2: Run SQL query"""
    query_result = db.sql_query(model_response)
    if prints == True:
        print(f"SQL Query result:\n{query_result}")
    return query_result


def step3_interpret_query(query_result, prints=False):
    """Step 3: Interpret SQL query results and provide a final answer and next step instruction."""
    rag_answer = model.model_response(
        question=query_result, template=interpret_query(), query_result=query_result, temperature=0
    )
    if prints == True:
        print(f"\n\n\nRAG ANSWER:\n{rag_answer}\n")
    return rag_answer


def rag(question, prints=False):
    """Full pipeline to answer a database related question using RAG model."""
    model_response = step1_text_to_sql(question, prints)
    query_results = step2_sql_query(model_response, prints)
    rag_answer = step3_interpret_query(query_results, prints)
    return rag_answer


if __name__ == "__main__":
    question = """
    Extract police MURDER type crime scene reports from 'SQL City' at 15 january 2018
    """
    print(rag(question))
