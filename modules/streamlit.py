import streamlit as st

import modules.database.db as db
from modules.ai.prompt_templates import conclude, text_to_query
from rag_pipeline import launch_model


def rag_translate(question):
    """
    Launch model to translate text to SQL query
    """
    model_response = launch_model("SQL Translator", question, text_to_query())
    st.write("Translator model Response:")
    st.write(model_response)
    return model_response


def db_query(query):
    """Run generated query"""
    query_results_df = db.streamlit_sql_query(query)
    st.write("SQL Query Results:")
    st.dataframe(query_results_df, height=200)
    query_results = db.query_result_to_string(query_results_df)
    return query_results


def rag_detective(query_results):
    """Run Detective model to analyze query results"""
    rag_answer = launch_model("Detective", query_results, conclude())
    st.write("RAG Answer:")
    st.write(rag_answer)
