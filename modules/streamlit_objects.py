import os
import subprocess

import streamlit as st

from modules.ai.model import model_response
from modules.database.db_functions import execute_sql_query
from modules.database.sql_functions import (
    convert_query_result_to_string,
    extract_query_from_string,
)


def rag_container():
    """
    Streamlit container for the RAG model.
    Shows a text area to enter a question and a button to get the answer.
    Pressing the button will trigger the RAG pipeline.
    """
    question = st.text_area("Enter your question here:", height=150)
    if st.button("Get Answer"):
        with st.spinner("Processing..."):
            streamlit_rag_pipeline(question)


def streamlit_rag_pipeline(question):
    """Full pipeline to answer a database related question using RAG model, with Streamlit display."""

    # Step 1: Translate text instructions into SQL query
    generated_answer = translator_container(question)

    st.divider()

    # Step 2: Execute the SQL query and display the results in a separate container
    query_results = extract_and_execute_query_container(generated_answer)

    st.divider()

    # Step 3: Launch the Detective model with the query results and display the final answer in a separate container
    detective_container(query_results)


def translator_container(question):
    """
    Launch model to translate text to SQL query
    """
    with st.container():
        model_answer = model_response(model_type="SQL Translator", question=question)
        st.write("Translator model Response:")
        st.write(model_answer)
        return model_answer


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


def get_demo_questions(file_path="files/demo_rag_questions.txt"):
    """
    Read demo questions from a file and return them as a list of strings.
    """
    questions = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            questions = file.readlines()
        # Remove any trailing newline characters
        questions = [question.strip() for question in questions]
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
    return questions


def demo_questions_button():
    if st.button("Demo questions"):
        # Display demo questions from txt file
        demo_question = get_demo_questions()
        for question in demo_question:
            st.write(question)


def how_does_it_work_button():
    if st.button("How does it work?"):
        st.image("files\\sql-agent.png", caption="SQL Agent")
