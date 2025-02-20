import pandas as pd
import streamlit as st

from modules.database.db import execute_sql_query
from modules.new_model import Translator


def chatbot():
    """Main chatbot function."""
    game_rules_sidebar()
    initialize_chat_session()
    display_chat_input()
    with st.container():
        show_chat_history()
    rag_pipeline()


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
            if message["role"] == "database":
                show_query_results()
            if message["role"] == "assistant":
                show_thinking_process()


def rag_pipeline():
    """Main RAG pipeline."""
    if st.session_state.current_state == "translator":
        translate_question()
    if st.session_state.current_state == "database":
        execute_query()
    if st.session_state.current_state == "detective":
        detective_conclusion()


def translate_question():
    """Translate the natural question to SQL query"""
    with st.spinner("Translating to SQL..."):
        question = st.session_state.context["user_inputs"][-1]
        translation = Translator(question=question)
        update_messages("database", translation.answer)
        update_context("sql_queries", translation.answer)
        update_current_state("database")
        st.rerun()


def execute_query():
    """Execute SQL query and return results."""
    with st.spinner("Executing SQL query..."):
        query = st.session_state.context["sql_queries"][-1]
        query_results = execute_sql_query(query)
        update_context("query_results", query_results)
        update_current_state("detective")
        st.rerun()


def detective_conclusion():
    """Detective's conclusion."""
    with st.spinner("Detective is analyzing the results..."):
        # last_question = st.session_state.context["user_inputs"][-1]
        # last_query_results = st.session_state.context["query_results"][-1]
        # detective = Detective(question=last_question, context=last_query_results)
        # update_messages("assistant", detective.answer)
        # update_context("detective_answers", detective.answer)
        # update_context("detective_thinking", detective.thinking)
        update_current_state(None)
        st.rerun()


def update_context(key, value):
    st.session_state.context[key].append(value)


def update_messages(role, content):
    st.session_state.messages.append({"role": role, "content": content})


def show_query_results():
    """Display query results as DataFrame."""
    if not st.session_state.context["query_results"]:
        return
    with st.expander("Query Results"):
        results = st.session_state.context["query_results"][-1]
        if isinstance(results, str) and results != "No valid SQL query found in the response.":
            df = convert_results_to_dataframe(results)
            st.dataframe(df)
        else:
            st.write(results)


def convert_results_to_dataframe(results):
    """Convert query results to DataFrame."""
    rows = results.strip().split("\n")
    headers = rows[0].replace("COLUMNS:", "").split(",")
    records = [eval(row) for row in rows[1:]]
    df = pd.DataFrame(records, columns=headers)
    return df


def update_current_state(state):
    st.session_state.current_state = state


def show_thinking_process():
    """Display detective's thinking process in expandable section."""
    with st.expander("Detective's Thinking Process"):
        st.write(st.session_state.context["detective_thinking"][-1])


def game_rules_sidebar():
    """Displays game rules & hints in the sidebar."""
    st.sidebar.title("Game Rules")
    st.sidebar.markdown("• Be concise\n• Only share relevant details\n• Stay in character")
