from modules.new_model import Detective, Translator

response = Translator("What is the name of the suspect?")
print("\n\n\n\n\n\n")

conclusion = Detective(response.response)

print(conclusion.response)
