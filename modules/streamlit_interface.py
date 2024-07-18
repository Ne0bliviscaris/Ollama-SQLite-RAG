from streamlit import title

from modules.streamlit_objects import (
    demo_questions_button,
    how_does_it_work_button,
    rag_container,
)


def streamlit_interface():
    # Streamlit UI title
    title("SQL RAG - local Ollama - Langchain")

    rag_container()

    demo_questions_button()

    how_does_it_work_button()
