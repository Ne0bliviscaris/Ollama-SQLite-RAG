import json

from modules.model import Detective

# question = "find last house on Franklin Ave"
# question = "find people living in the house with the largest address number on street named 'Franklin Ave'"

question = "there was a 'murder' in 'SQL City' on 'january 15, 2018'. Find the report, i want to find any clues"
context = r"""
{"user_inputs":["there was a 'murder' in 'SQL City' on 'january 15, 2018'. Find the report, i want to find any clues"],"sql_queries":["SELECT * FROM crime_scene_report WHERE date = '20180115' AND type = 'murder'"],"query_results":[[{"date":20180115,"type":"murder","description":"Life? Dont talk to me about life.","city":"Albany"},{"date":20180115,"type":"murder","description":"Mama, I killed a man, put a gun against his head...","city":"Reno"},{"date":20180115,"type":"murder","description":"Security footage shows that there were 2 witnesses. The first witness lives at the last house on \"Northwestern Dr\". The second witness, named Annabel, lives somewhere on \"Franklin Ave\".","city":"SQL City"}]]}
"""

context_dict = json.loads(context.strip())
query_results = context_dict["query_results"][0]
response = Detective(question, query_results)


print((response.full_response))
print("\nAnswer:\n", response.answer)
print("\nNext step:\n", response.next_step)
print("\nThinking:\n", response.thinking)
print("\nRules:\n", response.rules)
print("\nPrompt:\n", response.prompt())
# print("\nContext:\n", response.context)
