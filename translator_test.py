from modules.model import Translator

response = Translator("find all murder cases from SQL City")
# response = Translator("Find who lives in the last house in Franklin Ave. Order house numbers")
# response = Translator("Find who lives on the Franklin Ave")
# response = Translator("find all people with blue eyes. drivers_license has info about eye color")
# response = Translator("find names of all people with blue eyes. Eyes color is in drivers_license table")
# response = Translator("find all people with blue eyes. 'drivers_license' table has info about 'eye_color'")
# response = Translator("show all police murder case reports")


print((response.full_response))
print("\nQuery:\n", response.sql_query)
print("\nThinking:\n", response.thinking)
# print("Prompt:\n", response.prompt())
