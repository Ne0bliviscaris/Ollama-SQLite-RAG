import db
import model
from files.prompt_templates import interpret_query, text_to_query

# Manual query test
# db.sql_query(
#     """
# SELECT DISTINCT p.name AS witness_name, c.city AS crime_location
#     FROM crime_scene_report AS c
#     JOIN (SELECT * FROM person WHERE address_street_name = 'Northwestern Dr' AND address_number = (SELECT MAX(address_number) FROM person WHERE address_street_name = 'Northwestern Dr')) AS p1
#     ON c.city = p1.city
#     JOIN (SELECT * FROM person WHERE name = 'Annabel') AS p2
#     ON c.city = p2.city;
# """
# )

# STEP 1 - Generate SQL query using AI model
question = """
Extract police MURDER type crime scene reports from 'SQL City' at 15 january 2018
"""
model_response = model.model_response(question, template=text_to_query(), temperature=0)
print(f"\nQuestion: \n{question}")
print(f"Model answer:\n{model_response}")


# STEP 2 - Pass the AI generated query straight to database
query_result = db.sql_query(model_response)
print(f"\n{query_result}")

# STEP 3 - Let AI interpret the qury results
rag_answer = model.model_response(query_result, template=interpret_query(), temperature=0)
print(f"\n{rag_answer}\n")
