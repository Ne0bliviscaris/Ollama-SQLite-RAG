import streamlit as st

from modules.streamlit import process_sql_query, rag_detective, rag_translate


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


def update_chat_history(role: str, content: str):
    """Add new message to chat history with specified role."""
    st.session_state.messages.append({"role": role, "content": content})


def chatbot(user_input: str):
    """Process user input through RAG pipeline."""
    model_answer = process_user_input(user_input)

    sql_query, query_content = process_sql_query(model_answer)

    update_query_context(sql_query=sql_query, query_content=query_content)

    detective_answer, detective_thinking = rag_detective(query_content)
    process_detective_results(detective_answer, detective_thinking)


def process_detective_results(detective_answer, detective_thinking):
    """Process detective results and update chat history."""
    update_chat_history("assistant", detective_answer)
    st.session_state.context["detective_answers"].append(detective_answer)
    st.session_state.context["detective_thinking"].append(detective_thinking)


def update_query_context(sql_query, query_content):
    """Process SQL query and return results."""
    # Zapisz wyniki SQL
    if not sql_query:
        sql_query = "No valid SQL query found in the response."
    if not query_content:
        query_content = "No results found."

    update_chat_history("system", f"SQL Query: {sql_query}")
    st.session_state.context["sql_queries"].append(sql_query)
    st.session_state.context["query_results"].append(query_content)


def process_user_input(user_input: str):
    """Process user input and update chat history."""
    update_chat_history("user", user_input)
    st.session_state.context["user_inputs"].append(user_input)

    # Przetłumacz na SQL
    model_answer, _ = rag_translate(user_input)
    return model_answer


def chat():
    """Chatbot interface."""
    st.title("SQL Detective Chatbot")
    initialize_chat_session()

    # Chat input
    if prompt := st.chat_input("Ask about the case..."):
        chatbot(prompt)

    with st.container():
        show_chat_history()

    # # Debug view (opcjonalnie)
    # with st.expander("Debug: Session State"):
    #     st.write(st.session_state)


def show_chat_history():
    """Show chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "system":
                show_query_results()
            if message["role"] == "assistant":
                show_thinking_process()


def show_query_results():
    """Display SQL query results in expandable section."""
    with st.expander("SQL Query Results"):
        st.write(st.session_state.context["query_results"][-1])


def show_thinking_process():
    """Display detective's thinking process in expandable section."""
    with st.expander("Detective's Thinking Process"):
        st.write(st.session_state.context["detective_thinking"][-1])


chat()
