import requests

def chat_with_ollama(message):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'mistral',  # or llama3, gemma, deepseek-coder, etc.
            'prompt': message,
            'stream': False
        }
    )
    return response.json()['response']

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    reply = chat_with_ollama(user_input)
    print("Bot:", reply)
