import streamlit as st

from modules.ai.model import model_response, split_model_answer
from modules.database.db import execute_sql_query
from modules.database.query_tools import extract_sql_query
from modules.streamlit import process_sql_query, rag_detective, rag_translate


def update_context(key, value):
    st.session_state.context[key].append(value)


def update_messages(role, content):
    st.session_state.messages.append({"role": role, "content": content})


def initialize_chat_session():
    """Initialize chat session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "context" not in st.session_state:
        st.session_state.context = {
            "user_inputs": [],
            "sql_queries": [],
            "query_results": [],
            "detective_answers": [],
            "detective_thinking": [],
        }
    if "current_state" not in st.session_state:
        st.session_state.current_state = None


def display_chat_input():
    if prompt := st.chat_input("Ask about the case..."):
        st.session_state.current_state = "translator"
        update_context("user_inputs", prompt)
        update_messages("user", prompt)
        st.rerun()


def show_chat_history():
    """Show chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "translator":
                show_query_results()
            if message["role"] == "assistant":
                # show_thinking_process() of the detective
                ...


def rag_pipeline():
    """Main RAG pipeline."""
    display_chat_input()
    if st.session_state.current_state == "translator":
        translate_question()
    if st.session_state.current_state == "database":
        execute_query()


def translate_question():
    """Translate the natural question to SQL query"""
    question = st.session_state.context["user_inputs"][-1]
    generated_answer = model_response(model_type="SQL Translator", question=question)
    generated_answer, thinking_process = split_model_answer(generated_answer)
    extracted_query = extract_sql_query(generated_answer)
    update_messages("translator", extracted_query)
    update_context("sql_queries", extracted_query)
    st.session_state.current_state = "database"
    st.rerun()


def execute_query():
    """Execute SQL query and return results."""
    query = st.session_state.context["sql_queries"][-1]
    query_results = execute_sql_query(query)
    update_context("query_results", query_results)

    st.session_state.current_state = "detective"
    st.rerun()


def show_query_results():
    """Display query results as DataFrame."""
    with st.expander("Query Results"):
        if st.session_state.context["query_results"]:
            # Konwersja string wyników na DataFrame
            results = st.session_state.context["query_results"][-1]
            if isinstance(results, str) and results != "No valid SQL query found in the response.":
                # Rozdziel nazwy kolumn i dane
                lines = results.strip().split("\n")
                columns = lines[0].replace("COLUMNS:", "").split(",")

                # Konwersja pozostałych linii na DataFrame
                rows = [eval(row) for row in lines[1:]]
                import pandas as pd

                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(df)
            else:
                st.write(results)


def main():
    initialize_chat_session()
    with st.container():
        show_chat_history()
    rag_pipeline()

    st.write(st.session_state)


main()
