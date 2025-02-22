from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from modules.database.db import get_db_schema

# MODEL = "deepseek-r1:1.5b"
MODEL = "llama3.2:1b"
fake_key = "insert_anything_here"


class PydanticModelBase:
    def __init__(self, user_input):
        self.user_input = user_input
        self.agent = self.setup_agent()
        self.full_response = self.get_response()
        # self.answer, self.thinking = self.model_output()

    def get_response(self):
        return self.agent.run_sync(self.user_input)


class Translator(PydanticModelBase):
    def setup_agent(self):
        system_prompt = self._system_prompt()
        ollama_model = OpenAIModel(
            model_name=MODEL,
            base_url="http://localhost:11434/v1",
            api_key=fake_key,
            system_prompt_role=system_prompt,
        )
        return Agent(model=ollama_model, result_type=SQL_Query, retries=5)

    def _system_prompt(self):
        """System message for Translator model"""
        table_info = get_db_schema()
        dialect = "SQLite"
        return f"""
            **ROLE:** You are a SQL Translator. Your task is to translate the following question into a valid SQL query. Use {dialect} dialect.

            **Database Schema:**
            {table_info}

            **Rules:**
            1. Ensure the output contains a valid SQL query.
            2. The query must strictly follow the provided database schema and use only the available tables and columns.
            3. Keep the reasoning brief, ensuring it logically aligns with the user input.
            4. Avoid unnecessary complexity—only join tables or include conditions that are directly relevant to the user's question.
            5. Fetch all columns by default using 'SELECT *', unless a specific column is mentioned in the input.
            6. Be flexible in interpreting imprecise or incomplete user input while providing a valid SQL query.
            7. Do not use your own knowledge or external sources.
            8. Do not assume anything that is not explicitly present in the schema.
            9. ONLY return the SQL query, no additional explanations or text.
            10. If the user is asking about the order of items (first, last etc.), use an ORDER BY clause based on the relevant column.
            """


class SQL_Query(BaseModel):
    """Model for SQL query output with reasoning process."""

    sql_query: str = Field(
        description="Valid SQL query following the database schema",
        examples=[
            "SELECT * FROM crime_scene_report WHERE type = 'murder'",
            "SELECT * FROM person WHERE address_street_name = 'Franklin Ave' ORDER BY address_number DESC LIMIT 1",
            "SELECT * FROM interview WHERE person_id IN (SELECT id FROM person WHERE name LIKE '%Smith%')",
        ],
    )

    model_config = {
        "title": "SQL Translation Output",
        "description": "Structure for SQL query with explanation",
        "json_schema_extra": {
            "type": "object",
            "required": ["sql_query"],
            "properties": {
                "sql_query": {
                    "type": "string",
                    "description": "Valid SQL query starting with SELECT",
                    "pattern": "^SELECT.*",
                    "minLength": 20,
                },
            },
            "examples": [
                {
                    "sql_query": "SELECT * FROM crime_scene_report WHERE type = 'murder'",
                }
            ],
        },
    }
