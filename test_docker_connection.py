# Test the connection with local Ollama container
import time

from langchain_community.llms.ollama import Ollama

from modules.settings import MODEL, MODEL_URL

llm = Ollama(model=MODEL, base_url=MODEL_URL, temperature=0)

# Start timer before invoking
start_time = time.time()

response = llm.invoke("Say hello, answer with max 10 words.")

# End timer after invoking
end_time = time.time()

# Calculate response time
response_time = end_time - start_time

print(f"Model response {MODEL}: {response}")
print(f"Model response time {MODEL}: {response_time:.2f} sekund")
