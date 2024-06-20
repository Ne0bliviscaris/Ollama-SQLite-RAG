import db_connect
import model_connect

# db_query = "select * from person"
# db_query = """
# select * from crime_scene_report where date = '20180115' and city = 'SQL City'
# """
# db_connect.sql_query(db_query)


question = """
Retrieve murder crime scene report from police department's database from jan.15, 2018 in SQL City
"""
model_response = model_connect.prompt(question)
print(model_response)
