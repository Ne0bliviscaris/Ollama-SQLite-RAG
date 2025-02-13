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

        st.header("Translator model Response:")
        with st.spinner("Processing the question"):
            generated_answer = model_response(model_type="SQL Translator", question=question)
            generated_answer, thinking_process = split_model_answer(generated_answer)
            st.write(generated_answer)
            with st.expander(label="Thinking process"):
                st.write(thinking_process)

        st.divider()

        st.header("Translated query results:")
        extracted_query = extract_sql_query(generated_answer)
        st.write(f"SQL Query extracted from model's answer:\n{extracted_query}")
        query_results_df = execute_sql_query(extracted_query)
        with st.expander(label="Query Results:"):
            st.dataframe(query_results_df)

        st.divider()
        st.header("Detective's conclusion:")
        with st.spinner("Analyzing the results"):
            results_string = query_results_df.to_string(index=False)
            detective_answer = model_response(model_type="Detective", question=results_string)
            with st.expander(label="Detective model Response:"):
                st.write(detective_answer)
