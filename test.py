from modules.new_model import Translator

# from modules.PydanticAI import Translator

# response = Translator("find all murder cases from SQL City")
# response = Translator("Find who lives in the last house in Franklin Ave")
response = Translator("Find who lives on the Franklin Ave")
# response = Translator("find all car divers")
try:
    print("user_input:\n" + response.full_response["user_input"])
    print("\nquery:\n" + response.full_response["sql_query"])
    print("\nthinking:\n" + response.full_response["thinking"])
    print("\nrules_followed:\n" + response.full_response["rules_followed"])
except:
    print("\n\n" + response.full_response)


# print(json.dumps(response.full_response, indent=2))
# print("\n\n\n")
# print(response.answer)
# print("\n\n\n")

# conclusion = Detective(response.response)

# print(response.sql_query)
# print("\n\n\n")
# print(response.template)
