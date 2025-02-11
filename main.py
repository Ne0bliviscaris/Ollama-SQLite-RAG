import os
import subprocess

from streamlit import title

from modules.streamlit import rag


def main():
    title("SQL RAG - local Ollama - Langchain")

    rag()


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
