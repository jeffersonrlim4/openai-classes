import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

messages = [
  {'role': 'user', 'content': 'O que é uma maçã em 5 palavras'}
]

def generate_text(messages, model='gpt-4o-mini', max_tokens=1000, temperature=0):
  response = client.chat.completions.create(messages=messages, model=model, max_tokens=max_tokens, temperature=temperature)
  # resposta = response.choices[0].message.content
  resposta = response.choices[0].message.model_dump(exclude_none=True)
  
  messages.append(resposta)
  return messages

mensagens = generate_text(messages)

print(messages)