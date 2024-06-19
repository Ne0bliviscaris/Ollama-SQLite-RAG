import db_connect
import model_connect

db_connect.sql_query("SELECT * from person")


question = "How many people are there?"
model_connect.prompt(question)
