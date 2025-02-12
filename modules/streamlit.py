import streamlit as st

from modules.ai.model import model_response
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

        st.header("Translator model Response:")
        with st.spinner("Processing the question"):
            generated_answer = model_response(model_type="SQL Translator", question=question)
            with st.expander(label="Show full response"):
                st.write(generated_answer)

        st.divider()

        st.header("Translated query results:")
        extracted_query = extract_sql_query(generated_answer)
        st.write(f"SQL Query extracted from model's answer:\n{extracted_query}")
        query_results_df = execute_sql_query(extracted_query)
        with st.expander(label="Query Results:"):
            st.write(query_results_df)

        st.divider()
        st.header("Detective's conclusion:")
        with st.spinner("Analyzing the results"):
            detective_answer = model_response(model_type="Detective", question=query_results_df)
            with st.expander(label="Detective model Response:"):
                st.write(detective_answer)
