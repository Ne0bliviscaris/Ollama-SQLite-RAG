import json
import re

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from modules.database.db import db_without_solution, get_db_schema
from modules.settings import MODEL
from modules.tools import model_answer_regex


class Model:
    """Base class for all models."""

    def __init__(self, user_input, context=None):
        self.user_input = user_input
        self.context = context
        self.full_response = self.get_model_response()
        self.sql_query = self.get_field("sql_query")
        self.answer = self.get_field("answer")
        self.next_step = self.get_field("next_step")
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
            return self.full_response.get(field)

        if isinstance(self.full_response, str):
            return model_answer_regex(self.full_response, field)
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


class Detective(Model):
    """SQL Translator model class."""

    def model_input(self):
        return {
            "input": self.context,
            "question": self.user_input,
        }

    def template(self) -> str:
        """Prompt template to translate text instructions into SQL query"""
        detective = """
        **ROLE:** You are a detective. You are trying to solve a murder case and search for clues. Analyze received information in reference to received question. Please provide a concise, focused conclusion. Then provide next logical step to solve the mystery.

        **Rules:**
        1. Ensure the output contains answer and next_steps.
        2. Keep the thinking process brief, ensuring it logically aligns with the user input and context.
        3. Do not use your own knowledge or external sources.
        4. Do not assume anything that is not explicitly stated.

        
        **Input:** {input}{question}

        **Context:** {input}

        **Output:**
        ```json
        {{
            "question": "{question}",
            "answer": "Concise conclusion here."
            "next_step": "Next step to progress the case."
            "thinking": "Thinking process.",
            "rules_followed": "Rules followed while generating answer."
        }}
        top_k: {top_k}
        ```
        """
        return PromptTemplate(
            template=detective,
            input_variables=["input", "question"],
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
