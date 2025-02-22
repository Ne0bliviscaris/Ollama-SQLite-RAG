import json

from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from modules.database.db import database_connect, get_db_schema
from modules.settings import MODEL, TOKENS_LIMIT, TOP_K, TOP_P


class Model:
    """Base class for all models."""

    def __init__(self, user_input, context=None):
        self.user_input = user_input
        self.context = context
        self.full_response = self.get_model_response()
        self.answer, self.thinking = self.format_response()

    def model_config(self):
        """Static part of model configuration"""
        return {
            "model": MODEL,
            "num_predict": TOKENS_LIMIT,
            "top_p": TOP_P,
            "top_k": TOP_K,
            "format": "json",
        }

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

    def format_response(self):
        """Format the response from the model."""
        try:
            if isinstance(self.full_response, str):
                return None, None
            answer = self.full_response.get("sql_query", None)
            thinking = self.full_response.get("thinking", None)
            return answer, thinking

        except Exception as e:
            return f"Response formatting error. Model response:\n{self.full_response}", None


class Translator(Model):
    def model_input(self):
        return {
            "input": self.user_input,
            "question": self.user_input,
            "top_k": 5,
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
    

        
        **Input:** {input}

        **Output:**
        ```json
        {{
            "thinking": "Thinking process.",
            "sql_query": "SELECT * FROM table_name WHERE condition LIMIT {top_k};"
        }}
        ```
        """
        return PromptTemplate(
            template=translator,
            input_variables=["input", "top_k"],
            partial_variables={
                "dialect": "sqlite",
                "table_info": get_db_schema(),
            },
        )

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        db = database_connect()
        llm = ChatOllama(temperature=0, **self.model_config())
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
