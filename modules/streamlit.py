import streamlit as st

from modules.ai.model import model_response, split_model_answer
from modules.database.db import execute_sql_query
from modules.database.query_tools import extract_sql_query


def rag():
    """
    Streamlit container for the RAG model.
    Shows a text area to enter a question and a button to get the answer.
    Pressing the button will trigger the RAG pipeline.
    """
    question = st.text_area("Enter your question here:", height=150)
    if st.button("Get Answer"):
        with st.container(key="Translator"):
            st.header("Translator model Response:")
            generated_answer, thinking_process = rag_translate(question)

            st.write(generated_answer)
            with st.expander(label="Thinking process"):
                st.write(thinking_process)

        with st.container(key="Query Results"):
            st.divider()
            st.header("Translated query:")
            extracted_query, query_results = process_sql_query(generated_answer)
            st.write(extracted_query)
            query_results = execute_sql_query(extracted_query)
            with st.expander(label="Query Results:"):
                st.write(query_results)

        with st.container(key="Detective"):
            st.divider()
            st.header("Detective's conclusion:")

            with st.spinner("Analyzing the results"):
                detective_answer, thinking_process = rag_detective(query_results)
                st.write(detective_answer)
                with st.expander(label="Thinking process"):
                    st.write(thinking_process)


def rag_translate(question):
    """Translate the natural question to SQL query"""
    generated_answer = model_response(model_type="SQL Translator", question=question)
    generated_answer, thinking_process = split_model_answer(generated_answer)
    return generated_answer, thinking_process


def rag_detective(query_results_list):
    """Detective's conclusion"""
    detective_answer = model_response(model_type="Detective", question=query_results_list)
    answer, thinking_process = split_model_answer(detective_answer)
    return answer, thinking_process


def process_sql_query(model_answer):
    """Handle the SQL query received from the model"""
    extracted_query = extract_sql_query(model_answer)
    query_results = execute_sql_query(extracted_query)
    return extracted_query, query_results
