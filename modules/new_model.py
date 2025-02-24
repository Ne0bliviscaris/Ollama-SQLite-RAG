import json
import re

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from modules.database.db import db_without_solution, get_db_schema
from modules.settings import MODEL


class Model:
    """Base class for all models."""

    def __init__(self, user_input, context=None):
        self.user_input = user_input
        self.context = context
        self.full_response = self.get_model_response()
        self.sql_query = self.get_field("sql_query")
        self.thinking = self.get_field("thinking")

    def get_model_response(self):
        """Get response using instance attributes."""
        try:
            langchain = self.build_langchain()
            response_str = langchain.invoke(self.model_input())
            try:
                parsed_response = json.loads(response_str)
                return parsed_response
            except:
                return response_str
        except Exception as e:
            return f"Model Connection error. Make sure Ollama is running and {MODEL} is installed.\n{e}"

    def get_field(self, field=None):
        """Get SQL query from parsed_response."""
        if isinstance(self.full_response, dict):
            try:
                return self.full_response[field]
            except:
                return None

        if isinstance(self.full_response, str):
            regex = (
                rf'"{field}"'  # "field"
                r"\s*:\s*"  # : (with optional spaces)
                r'"'  # opening "
                r'([^"]*)'  # any characters except "
                r'(?:"|$)'  # ending " or end of string
            )
            match = re.search(regex, self.full_response, re.VERBOSE)
            if match:
                return match.group(1)
        return None

    def get_thinking_process(self):
        """Get thinking process from parsed_response."""
        return self.response_json.get("thinking")


class Translator(Model):
    """SQL Translator model class."""

    def model_input(self):
        return {
            "input": self.user_input,
            "question": self.user_input,
        }

    def template(self) -> str:
        """Prompt template to translate text instructions into SQL query"""
        translator = """
        **ROLE:** You are a SQL Translator. Your task is to translate the following question into a valid SQL query. Use {dialect} dialect.

        **Database Schema:**
        {table_info}

        **Rules:**
        1. Ensure the output contains a valid SQL query.
        2. The query must strictly follow the provided database schema and use only the available tables and columns.
        3. Keep the thinking process brief, ensuring it logically aligns with the user input.
        4. Avoid unnecessary complexity—only join tables or include conditions that are directly relevant to the user's question.
        5. Fetch all columns by default using 'SELECT *', unless a specific column is mentioned in the input.
        6. Be flexible in interpreting imprecise or incomplete user input while providing a valid SQL query.
        7. Do not use your own knowledge or external sources.
        8. Do not assume anything that is not explicitly present in the schema.
        9. ONLY return the SQL query, no additional explanations or text.
        10. If the user is asking about the order of items (first, last etc.), use an ORDER BY clause based on the relevant column.
        11. While using columns from multiple tables, ensure you call proper tables.

        
        **Input:** {input}

        **Output:**
        ```json
        {{
            "user_input": "{input}",
            "sql_query": "SELECT * FROM table_name WHERE condition;"
            "thinking": "Thinking process.",
            "rules_followed": "Rules followed while generating answer."
        }}
        top_k: {top_k}
        ```
        """
        return PromptTemplate(
            template=translator,
            input_variables=["input"],
            partial_variables={
                "dialect": "sqlite",
                "table_info": get_db_schema(),
            },
        )

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        db = db_without_solution()
        llm = ChatOllama(
            temperature=0,
            seed=1,
            model=MODEL,
            # num_predict=128,  # Output tokens limit
            num_predict=512,  # Output tokens limit
            top_p=0.95,
            format="json",
            mirostat=2,
            mirostat_eta=2,
            mirostat_tau=1,
            tfs_z=50,  # reduce the impact of less probable tokens
            repeat_penalty=1.5,
            top_k=2,
        )
        prompt = self.template()
        return create_sql_query_chain(llm, db, prompt)


# class Detective(Model):

#     def template():
#         """Prompt template to interpret SQL query results and provide a final answer."""

#         detective = """
#         **ROLE:** You are a skilled detective. You are trying to solve a murder case and search for clues. Analyze received information. Interpret the results and provide a very concise, focused conclusion. Do not use any spare words.


#         **Input:**

#         - **Input:** "These are the received results you have to interpret"

#         Only write a short, concise conclusion.

#         - **Answer:** "Concise conclusion here."

#         **Only use the following tables:**

#         {table_info}

#         **Input:** {input}

#         **TopK:** {top_k}
#         """
#         prompt_template = PromptTemplate.from_template(detective)
#         return prompt_template

#     def template(self) -> str:
#         """Prompt template to translate text instructions into SQL query"""
#         translator = """
#         **ROLE:** You are a skilled detective. You are trying to solve a murder case and search for clues. Analyze received information. Interpret the results and provide a very concise, focused conclusion. Do not use any spare words.

#         **Database Schema:**
#         {table_info}

#         **Rules:**
#         1. Keep your thinking process short and concise.
#         2. You ONLY use tables and columns from the Database Schema
#         3. You do not use your own knowledge
#         4. You do not use any external sources of information
#         5. You do not use any spare words
#         6. ONLY return the SQLQuery to run.
#         7. Keep the query simple, but fetch all columns.
#         8. Do not assume anything that is not provided in the database schema.
#         9. Fetch all columns for detective to solve the case.

#         Translate the following user input:
#         **Input:** {input}


#         **Output:**
#         Return outputs in the following JSON format:
#         ```json
#         {{
#             "thinking": "Thinking process, if there is any."
#             "sql_query": "SELECT * FROM table_name WHERE condition;",
#         }}
#         top_k: {top_k}
#         ```
#         """
#         return PromptTemplate(
#             template=translator,
#             input_variables=["input", "question"],
#             partial_variables={
#                 "dialect": "sqlite",
#                 "top_k": TOP_K,
#                 "table_info": get_db_schema(),
#             },
#         )

#     def build_langchain(self):
#         """Builds and returns a language chain with database and Ollama connections."""
#         db = database_connect()
#         llm = ChatOllama(temperature=0, **self.model_config())
#         template = self.template()
#         return create_sql_query_chain(llm, db, template)
