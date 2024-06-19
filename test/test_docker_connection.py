# Test the connection with local Ollama container
from langchain_community.llms.ollama import Ollama

llm = Ollama(model="llama3", base_url="http://localhost:11434")

llm("Hello world")
