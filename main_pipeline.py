import connections
import model

# connections.sql_query(
#     """
# SELECT * FROM crime_scene_report WHERE city = 'SQL City' AND date = '20180115';
# """
# )


question = """
Extract police MURDER type crime scene reports from 'SQL City' at 15 january 2018
"""
model_response = model.process_query_and_get_response(question)
print(f"Question: {question}")
print(f"Model answer:\n{model_response}\n")
