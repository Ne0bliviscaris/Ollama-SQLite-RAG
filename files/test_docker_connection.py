# Test the connection with local Ollama container
from langchain_community.llms.ollama import Ollama
from settings import MODEL, MODEL_URL

llm = Ollama(model=MODEL, base_url=MODEL_URL)

response = llm.invoke("Hello world")
print(response)
