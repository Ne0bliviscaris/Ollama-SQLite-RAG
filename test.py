from modules.new_model import Translator

# from modules.PydanticAI import Translator

response = Translator("find all murder cases from SQL City")
# response = Translator("Find who lives in the last house in Franklin Ave. Order house numbers")
# response = Translator("Find who lives on the Franklin Ave")
# response = Translator("find all people with blue eyes. drivers_license has info about eye color")
# response = Translator("find names of all people with blue eyes. Eyes color is in drivers_license table")
# response = Translator("find all people with blue eyes. 'drivers_license' table has info about 'eye_color'")
# response = Translator("show all police murder case reports")
# try:
#     print("user_input:\n" + response.full_response["user_input"])
#     print("\nquery:\n" + response.full_response["sql_query"])
#     print("\nthinking:\n" + response.full_response["thinking"])
#     # print("\nrules_followed:\n" + response.full_response["rules_followed"])
# except:
# print("\n\n" + response.full_response + "\n\n")
print((response.full_response))
print("\n\n", response.sql_query)
print("\n\n", response.thinking)
# print((response.answer))


# print(json.dumps(response.full_response, indent=2))
# print("\n\n\n")
# print(response.answer)
# print("\n\n\n")

# conclusion = Detective(response.response)

# print(response.sql_query)
# print("\n\n\n")
# print(response.template)
