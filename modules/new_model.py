import json
import re

from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from modules.database.db import database_connect, get_db_schema
from modules.settings import MODEL


class Model:
    """Base class for all models."""

    def __init__(self, question):
        self.question = question
        self.template = None

    def model_config(self):
        """Static part of model configuration"""
        model = MODEL
        top_k = 1
        top_p = 0.01
        output_tokens_limit = 5000
        return {
            "model": model,
            "top_k": top_k if top_k else None,
            "num_predict": output_tokens_limit if output_tokens_limit else None,
            "top_p": top_p if top_p else None,
        }

    def _initialize(self):
        """Initialize chain and get response."""
        self.langchain = self.build_langchain()
        self.full_response = self.get_model_response()
        parsed_response = json.loads(self.full_response)
        self.sql_query = parsed_response

        # self.answer, self.thinking = self.split_model_answer(self.full_response)
        # return self.answer, self.thinking
        return self.sql_query

    def split_model_answer(self, model_answer: str) -> tuple[str, str]:
        """Split model output into thinking process and final answer."""
        # Szukamy znaczników <think> i </think>
        THINK_PATTERN = r"<think>(.*?)</think>"
        thinking_match = re.search(THINK_PATTERN, model_answer, re.DOTALL)
        if thinking_match:
            thinking = thinking_match.group(1).strip()
            answer = re.sub(THINK_PATTERN, "", model_answer, flags=re.DOTALL).strip()
        else:
            thinking = ""
            answer = model_answer.strip()

        return answer, thinking

    def get_model_response(self):
        """Get response using instance attributes."""
        try:
            return self.langchain.invoke(input={"question": self.question})
        except Exception as e:
            return f"Model Connection error. Make sure Ollama is running and {MODEL} is installed.\n{e}"


class Translator(Model):
    def __init__(self, question: str):
        self.question = question
        self.template = self.translator_template()
        super().__init__(question)
        self.sql_query = self._initialize()

    def role(self):
        """Set the role of the translator model."""
        return f"You are a SQL Translator. Your task is to translate the following question into a valid SQL query."

    def rules(self):
        """Define rules for the translator model."""
        return f"""
        1. You ONLY use tables and columns from the Database Schema
        2. You do not use your own knowledge
        3. You do not use any external sources of information
        4. You do not use any spare words
        5. ONLY return the SQLQuery to run.
        6. Keep the query simple and efficient
        7. Do not present the results of the query
        """

    def translator_template(self) -> str:
        """Prompt template to translate text instructions into SQL query"""
        translator = """
        **ROLE:** {role}. Use {dialect} dialect.
        
        **Database Schema:**
        {table_info}
        
        **Rules:**
        {rules}

        **Question:** {question}

        **Output:**
        Return outputs in the following JSON format:
        ```json
        {{
            "sql_query": "SELECT * FROM table_name WHERE condition;"
            "answer": "Anything not belonging to sql_query."
            "thinking": "Thinking process, if there is any."
        }}
        ```
        """
        return PromptTemplate.from_template(
            template=translator,
            partial_variables={
                "role": self.role(),
                "table_info": get_db_schema(),
                "dialect": "sqlite",
                "rules": self.rules(),
            },
        )

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        db = database_connect()
        llm = ChatOllama(temperature=0, **self.model_config(), format="json")
        template = self.translator_template()
        return create_sql_query_chain(llm, db, self.template)


class TranslatorOutputStructure(BaseModel):
    """Model for the output of the Translator class."""

    thinking_process: str
    response_text: str
    sql_query: str


class Detective(Model):
    def __init__(self, question: str):
        self.question = question
        self.template = self.detective_template()
        super().__init__(question)
        self.response, self.thinking_process = self._initialize()

    def detective_template():
        """Prompt template to interpret SQL query results and provide a final answer."""

        template = """
        **ROLE:** You are a skilled detective. You are trying to solve a murder case and search for clues. Analyze received information. Interpret the results and provide a very concise, focused conclusion. Do not use any spare words. 


        **Input:**

        - **Input:** "These are the received results you have to interpret"

        Only write a short, concise conclusion.

        - **Answer:** "Concise conclusion here."

        **Only use the following tables:**

        {table_info}

        **Input:** {input}

        **TopK:** {top_k}
        """
        prompt_template = PromptTemplate.from_template(template)
        return prompt_template

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        db = database_connect()
        llm = ChatOllama(temperature=1, **self.model_config())
        return create_sql_query_chain(llm, db, self.template)
