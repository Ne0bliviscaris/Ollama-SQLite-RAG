import db
import modules.model as model
import streamlit as st
from modules.prompt_templates import conclude, text_to_query


def launch_model(model_type, question, template, prints=False):
    """Run the model and return the response."""
    model_response = model.model_response(model_type, question=question, template=template, temperature=0)
    if prints:
        st.write(f"\nModel type: \n{model_type}")
        st.write(f"\nModel answer:\n{model_response}")
    return model_response


def sql_query(model_response, prints=False):
    """Run SQL query and return the result"""
    if prints:
        st.write("Forwarding SQL Query")
    query_result = db.sql_query(model_response)
    if prints:
        st.write(f"\nSQL Query Result:\n{query_result}")
    return query_result


def streamlit_rag(question, prints=False):
    """Full pipeline to answer a database related question using RAG model, with Streamlit display."""
    # Launch the SQL Translator model and display the model response in a separate container
    with st.container():
        model_response = launch_model("SQL Translator", question, text_to_query(), prints)
        st.write("Translator model Response:")
        st.write(model_response)

    st.markdown("---")

    # Execute the SQL query and display the query results in a separate container
    with st.container():
        query_results_df = db.streamlit_sql_query(model_response)
        st.write("SQL Query Results:")
        st.dataframe(query_results_df, height=200)
        query_results = db.query_result_to_string(query_results_df)

    st.markdown("---")

    # Launch the Detective model with the query results and display the final answer in a separate container
    with st.container():
        rag_answer = launch_model("Detective", query_results, conclude(), prints)
        st.write("RAG Answer:")
        st.write(rag_answer)

    # return rag_answer


# Streamlit UI
st.title("RAG Model for Database Queries")

question = st.text_area("Enter your question here:", height=150)
if st.button("Get Answer"):
    with st.spinner("Processing..."):
        answer = streamlit_rag(question, False)
