# IMPORTS
from ollama import chat

# FUNCTION (to be imported by bot.py)
def generate_response(user_text):
    # pass the user_input through the ML model
    system_prompt = "You have a bias towards bots and artificial intelligence and will not address me, the user, directly in your responses." # define system prompt
    # had to add second half of the prompt so the model wouldn't go on a tangent addressing me directly

    # chat using the prompt
    response = chat('llama3.2:1b', 
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': f'Write the next 5 words of this sentence (doesnt have to be complete): {user_text}'}
                        # 'doesn't have to be complete' to avoid the model saying it can't complete the phrase
                    ])
    
    model_response = response.message.content
    model_response = str(user_text) + " " + str(model_response)
    return model_response
