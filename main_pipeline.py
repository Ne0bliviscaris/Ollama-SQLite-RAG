import model

question = """
Retrieve murder crime scene report from police department's database from jan.15, 2018 in SQL City
"""
model_response = model.process_query_and_get_response(question)
print(model_response)
