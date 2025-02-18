import re

from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from modules.database.db import database_connect, get_db_schema
from modules.settings import MODEL


class Model:
    """Base class for all models."""

    def __init__(self, question):
        self.question = question
        self.langchain = None
        self.template = None
        self.langchain = None
        self.model_answer = None
        self.response = None
        self.thinking_process = None

    def model_config(self):
        """Static part of model configuration"""
        model = MODEL
        top_k = 1
        output_tokens_limit = 500
        return {"model": model, "top_k": top_k, "num_predict": output_tokens_limit}

    def _initialize(self):
        """Initialize chain and get response."""
        self.langchain = self.build_langchain()
        response = self.get_model_response()
        self.response, self.thinking_process = self.split_model_answer(response)
        return self.response, self.thinking_process

    def split_model_answer(self, model_answer: str) -> tuple[str, str]:
        """Split model output into thinking process and final answer."""
        # Szukamy znaczników <think> i </think>
        THINK_START = "<think>"
        content = "(.*?)"
        THINK_END = "</think>"
        think_pattern = rf"{THINK_START}{content}{THINK_END}"
        thinking = re.search(think_pattern, model_answer, re.DOTALL)
        self.thinking_process = thinking.group(1).strip() if thinking else ""
        self.output = re.sub(pattern=think_pattern, repl="", string=model_answer, flags=re.DOTALL).strip()
        return self.output, self.thinking_process

    def get_model_response(self):
        """Get response using instance attributes."""
        try:
            return self.langchain.invoke(self.instructions)
        except Exception as e:
            return f"Model Connection error. Make sure Ollama is running and {MODEL} is installed.\n{e}"


class Translator(Model):
    def __init__(self, question: str):
        self.question = question
        self.db_info = get_db_schema()
        self.role = self.set_role()
        self.instructions = self.instructions()
        self.template = self.translator_template()
        super().__init__(question)
        self.response, self.thinking_process = self._initialize()

    def set_role(self):
        """Set the role of the translator model."""
        return "You are a helpful SQL Translator. Given an input question, create a simple, syntactically correct {dialect} query to run."

    def instructions(self):
        """Instructions dict for the translator model."""
        instructions = {
            "question": self.question,
            "table_info": self.db_info,
            "input": self.question,
            "dialect": "sqlite",
        }
        return instructions

    def translator_template(self) -> str:
        """Prompt template to translate text instructions into SQL query"""
        template = f"""
        **ROLE:** {self.role}
        
        {self.instructions}

        **Only use the following tables:**
        {{table_info}}

        **Question:** {{input}}
        """
        return PromptTemplate.from_template(template)

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        db = database_connect()
        llm = ChatOllama(temperature=0, **self.model_config())
        return create_sql_query_chain(llm, db, self.template)


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
        llm = ChatOllama(model=MODEL, temperature=1, request_timeout=self.timeout)
        return create_sql_query_chain(llm, db, self.template)
