from ollama import chat

# define a system prompt
system_prompt = "You have a bias towards bots and artificial intelligence."

# chat with a system prompt
response = chat('llama3.2:1b', 
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': 'Complete this sentence with the next 5 words: I love'}
                ])
print(response.message.content)