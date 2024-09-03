import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

messages = [
  {'role': 'user', 'content': 'me conte uma história sobre atlântida'}
]

def generate_text(messages, model='gpt-4o-mini', max_tokens=1000, temperature=0, stream=True):
  response = client.chat.completions.create(messages=messages, model=model, max_tokens=max_tokens, temperature=temperature, stream=stream)
  
  for strem_response in response:
    text = strem_response.choices[0].delta.content
    if text:
      print(text, end='')
  
  # messages.append(resposta)
  # return messages

# mensagens = generate_text(messages)

# print(messages)

generate_text(messages)