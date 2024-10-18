import requests


api_endpoint = 'http://localhost:11434/api/chat'

messages = []

while True:
    # capture user input
    user_input = input('You: ')
    # updating messages
    messages.append({'role': 'user', 'content': user_input})
    # sending our inputs to AI
    data = {
        'model': 'llama2',
        'stream': False,
        'messages': messages
    }

    response = requests.post(api_endpoint, json=data)
    if response.status_code == 200:
        response_data = response.json()

        assistant_response = response_data['message']['content']

        # updating messages with response
        messages.append({'role': 'chatbot', 'content':
        assistant_response})

        # showing the response to the user
        print(f'Assistant: {assistant_response}')
    else:
        print('Failed to get response from Ollama API')