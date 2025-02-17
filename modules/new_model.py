from langchain.chains import create_sql_query_chain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

from modules.database.db import database_connect, get_db_schema
from modules.settings import MODEL, MODEL_TIMEOUT


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

    def _initialize(self):
        """Initialize chain and get response."""
        self.langchain = self.build_langchain()
        response = self.get_response()
        self.response, self.thinking_process = self.split_model_answer(response)
        return self.response, self.thinking_process

    def __repr__(self):
        question = self.question if self.question else "No question"
        response = self.response if self.response else "No response"
        thinking_process = self.thinking_process if self.thinking_process else "No thinking process"
        return f"Question: {question}\nResponse: {response}\nThinking Process: {thinking_process}"

    def split_model_answer(self, model_answer: str) -> tuple[str, str]:
        """Split model output into thinking process and final answer."""
        # Szukamy znaczników <think> i </think>
        THINK_START = "<think>"
        content = "(.*?)"
        THINK_END = "</think>"
        think_pattern = rf"{THINK_START}{content}{THINK_END}"
        import re

        thinking = re.search(think_pattern, model_answer, re.DOTALL)
        self.thinking_process = thinking.group(1).strip() if thinking else ""

        self.output = re.sub(pattern=think_pattern, repl="", string=model_answer, flags=re.DOTALL).strip()

        return self.output, self.thinking_process

    @classmethod
    def model_response(cls, question: str):
        """Launch the model and return the response."""
        instance = cls(question)
        return instance.get_response()

    def get_response(self):
        """Get response using instance attributes."""
        try:
            return self.langchain.invoke(self.instructions)
        except Exception as e:
            return f"Model Connection error. Make sure Ollama is running and {MODEL} is installed.\n{e}"

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        pass


class Translator(Model):
    def __init__(self, question: str):
        self.question = question
        # self.template = self.translator_template()
        self.role = """You are a skilled detective and data analyst. Given an input question, first create a syntactically correct {dialect} query to run."""
        self.instructions = self.instructions()
        self.template = self.test_template()
        super().__init__(question)
        self.response, self.thinking_process = self._initialize()

    def instructions(self):
        """Instructions dict for the translator model."""
        instructions = {
            "question": self.question,
            "template": self.translator_template(),
            "table_info": get_db_schema(),
            "input": self.question,
            "top_k": 1,
            "dialect": "sqlite",
        }
        return instructions

    def translator_template(self) -> str:
        """Prompt template to translate text instructions into SQL query"""

        template = """
        **ROLE:** You are a skilled detective and data analyst. Given an input question, first create a syntactically correct {dialect} query to run, ensuring it retrieves all relevant records without imposing unnecessary limits. Then, look at the results of the query and return the answer. Use the following format:


        **Input:**

        - **Question:** "Question here"
        - **SQLQuery:** "SQL Query to run"
        - **SQLResult:** "Result of the SQLQuery"
        - **Answer:** "Final answer here"

        **Only use the following tables:**

        {table_info}

        **Question:** {input}

        **TopK:** {top_k}
        """
        prompt_template = PromptTemplate.from_template(template)
        return prompt_template

    def test_template(self) -> str:
        """Prompt template to translate text instructions into SQL query"""
        template = f"""
        **ROLE:** {self.role}
        
        {self.instructions}

        **Only use the following tables:**
        {{table_info}}

        **Question:** {{input}}
        **TopK:** {{top_k}}
        """
        return PromptTemplate.from_template(template)

    def build_langchain(self):
        """Builds and returns a language chain with database and Ollama connections."""
        db = database_connect()
        llm = ChatOllama(model=MODEL, temperature=0, request_timeout=MODEL_TIMEOUT)
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
        llm = ChatOllama(model=MODEL, temperature=1, request_timeout=MODEL_TIMEOUT)
        return create_sql_query_chain(llm, db, self.template)
