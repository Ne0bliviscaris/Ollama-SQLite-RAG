import os
import subprocess

import streamlit as st

from modules.chatbot import chatbot


def title_screen():
    st.title("SQL RAG - local Ollama - Langchain")
    st.markdown(
        """
        Welcome to the SQL RAG chatbot! Ask about the case to get started.
        """
    )


def main():
    if not st.session_state:
        title_screen()
    chatbot()


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
