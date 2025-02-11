import streamlit as st

from modules.ai.model import model_response
from modules.database.db import execute_sql_query
from modules.database.query_tools import (
    convert_query_result_to_string,
    extract_query_from_string,
)


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
        with st.spinner("Executing the query"):
            query_results = extract_and_execute_query_container(generated_answer)
            with st.expander(label="Query Results:"):
                st.write(query_results)

        st.divider()
        st.header("Detective's conclusion:")
        with st.spinner("Analyzing the results"):
            detective_answer = model_response(model_type="Detective", question=query_results)
            with st.expander(label="Detective model Response:"):
                st.write(detective_answer)


def extract_and_execute_query_container(model_response):
    """Extract SQL query from model response and execute it"""
    with st.container():
        # Extract SQL query from model response
        extracted_query = extract_query_from_string(model_response)
        st.write("SQL Query extracted from model's answer:")
        st.write(extracted_query)
        # Execute SQL query
        query_results_df = execute_sql_query(extracted_query)
        st.write("SQL Query Results:")
        st.dataframe(query_results_df, height=200)
        # Convert query results to a string
        query_results_string = convert_query_result_to_string(query_results_df)
        return query_results_string


def detective_container(query_results):
    """Run Detective model to analyze query results"""
    with st.container():
        rag_answer = model_response(model_type="Detective", question=query_results)
        st.write("RAG Answer:")
        st.write(rag_answer)
