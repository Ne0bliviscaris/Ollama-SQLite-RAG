from modules.db import database_connect, sql_query

database = database_connect()
# Manual query test
results_string = sql_query(
    """
                           SELECT * FROM person where license_id = 993845 
                           limit 10"""
)
print(results_string)
