#### Newbie-friendly Readme will be made soon
---
### Issues to solve:
#### Unstructured model output. 
The model does not always obey given instructions. Potential solution to the problem will be to incorporate `Pydantic` BaseModel. More on this topic here: https://medium.com/@haldankar.deven/cracking-the-code-getting-structured-output-from-ollama-15652c4613e1

#### No context window
Every time the model is called, the context window gets reset. It happens because upon every model call, connection with model is rebuilt.

It happens twice per question:
  - once when you ask the question 
  - once when the model receives SQL output to interpret
