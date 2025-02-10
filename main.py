import os
import subprocess

from streamlit import title

from modules.streamlit_objects import (
    demo_questions_button,
    how_does_it_work_button,
    rag_container,
)


def main():
    title("SQL RAG - local Ollama - Langchain")

    rag_container()

    demo_questions_button()

    how_does_it_work_button()


if __name__ == "__main__":  # Poprawiono cudzysłowy
    # Launch streamlit and check if it's not already running
    if not os.environ.get("RUNNING_IN_STREAMLIT"):
        # Mark streamlit as running
        os.environ["RUNNING_IN_STREAMLIT"] = "1"
        file_path = os.path.abspath(__file__)
        # Run streamlit with correct command list
        subprocess.run(["streamlit", "run", file_path], check=True)
    else:
        main()
