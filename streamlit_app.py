import streamlit as st

import modules.db as db
from modules.ai.prompt_templates import conclude, text_to_query
from rag_pipeline import launch_model


def streamlit_rag(question, prints=False):
    """Full pipeline to answer a database related question using RAG model, with Streamlit display."""
    # Launch the SQL Translator model and display the model response in a separate container
    with st.container():
        model_response = launch_model("SQL Translator", question, text_to_query(), prints)
        st.write("Translator model Response:")
        st.write(model_response)

    # st.markdown("---")
    st.divider()

    # Execute the SQL query and display the query results in a separate container
    with st.container():
        query_results_df = db.streamlit_sql_query(model_response)
        st.write("SQL Query Results:")
        st.dataframe(query_results_df, height=200)
        query_results = db.query_result_to_string(query_results_df)

    # st.markdown("---")
    st.divider()

    # Launch the Detective model with the query results and display the final answer in a separate container
    with st.container():
        rag_answer = launch_model("Detective", query_results, conclude(), prints)
        st.write("RAG Answer:")
        st.write(rag_answer)

    # return rag_answer


# Streamlit UI
st.title("SQL RAG - local Ollama - Langchain")


question = st.text_area("Enter your question here:", height=150)
if st.button("Get Answer"):
    with st.spinner("Processing..."):
        answer = streamlit_rag(question, False)

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
