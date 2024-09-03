import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

def text_generate(messages):
  response = client.chat.completions.create(
    messages=messages, 
    model='gpt-4o-mini', 
    max_tokens=1000, 
    temperature=0, 
    stream=True
  )

  print('Assistant: ', end='')
  complet_text = '' 
  for item in response:
    text = item.choices[0].delta.content
    if text:
      complet_text += text
      print(text, end='')
  print('')
      
  messages.append({'role': 'assistant', 'content': complet_text})
  
  return messages

if __name__ == '__main__':
  print('Bem vindo ao JeffGPT')
  messages = []
  while True:
    user_input = input('User: ')
    
    if user_input == 'top':
      break
    
    messages.append({'role': 'user', 'content': user_input})
    messages = text_generate(messages)