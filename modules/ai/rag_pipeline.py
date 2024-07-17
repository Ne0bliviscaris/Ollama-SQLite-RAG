import modules.ai.model as model
import modules.database.db as db
from modules.ai.prompt_templates import conclude, text_to_query


def launch_model(model_type, question, template, prints=False):
    """Run the model and return the response."""
    model_response = model.model_response(model_type, question=question, template=template, temperature=0)

    # Print the user input and model response on demand
    if prints == True:
        print(f"\nModel type: \n{model_type}")
        print(f"\nModel answer:\n{model_response}")
    return model_response


def sql_query(model_response, prints=False):
    """Run SQL query and return the result"""

    if prints == True:
        print(f"Forwarding SQL Query")

    query_result = db.sql_query(model_response)

    # Print the SQL query result on demand
    if prints == True:
        print(f"\nSQL Query Result:\n{query_result}")
    return query_result
