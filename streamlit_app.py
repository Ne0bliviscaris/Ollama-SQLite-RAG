import streamlit as st

from modules.streamlit import db_query, rag_detective, rag_translate


def streamlit_rag(question):
    """Full pipeline to answer a database related question using RAG model, with Streamlit display."""

    # Step 1: Translate text instructions into SQL query
    with st.container():
        generated_query = rag_translate(question)

    st.divider()

    # Step 2: Execute the SQL query and display the results in a separate container
    with st.container():
        query_results = db_query(generated_query)

    st.divider()

    # Step 3: Launch the Detective model with the query results and display the final answer in a separate container
    with st.container():
        rag_detective(query_results)


# Streamlit UI
st.title("SQL RAG - local Ollama - Langchain")


question = st.text_area("Enter your question here:", height=150)
if st.button("Get Answer"):
    with st.spinner("Processing..."):
        answer = streamlit_rag(question)

if st.button("Demo questions"):
    st.write(
        """
Extract police MURDER type crime scene reports from 'SQL City' at 15 january 2018
 

The witness resides at the last house on "Northwestern Dr"


find who lives in 'Northwestern Dr', 4919


find out more about Christopher Peteuil with license ID 993845

Which city has the highest crime rate?

"""
    )
if st.button("How does it work?"):
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*71lI66X4-4nxkKWVhrTW_A.png", caption="SQL Agent")


# LAUNCH STREAMLIT DIRECTLY
import os
import subprocess

# Launch streamlit and check if it's not already running
if __name__ == "__main__" and not os.environ.get("RUNNING_IN_STREAMLIT"):
    # Mark streamlit as running
    os.environ["RUNNING_IN_STREAMLIT"] = "1"
    # Get file path
    file_path = os.path.abspath(__file__)
    # Run streamlit
    subprocess.run(["streamlit", "run", file_path], check=True)
