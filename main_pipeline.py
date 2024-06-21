import db
import model

# Manual query test
# connections.sql_query(
#     """
# SELECT * FROM crime_scene_report WHERE city = 'SQL City' AND date = '20180115';
# """
# )

# STEP 1 - Generate SQL query using AI model
question = """
Extract police MURDER type crime scene reports from 'SQL City' at 15 january 2018
"""
model_response = model.model_response(question)
# print(f"Question: {question}")
# print(f"Model answer:\n{model_response}\n")


# STEP 2 - Pass the AI generated query straight to database
query_result = db.sql_query(model_response)
