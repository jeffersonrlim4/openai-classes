#introdução a assistentes de ai
import openai
import time
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

#criar o assistant
assistant = client.beta.assistants.create(
  name="Tutor de matemática do Colégio Positivo",
  instructions="Você é um tutor pessoal de matemática do Colégio Positivo. \
                Escreva e execute códigos para responder as perguntas de matemática que lhe forem passadas.",
  tools=[{"type": "code_interpreter"}],
  model='gpt-4o-mini'
)

#criar a thread
thread = client.beta.threads.create()

#criar mensagem para a thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role='user',
  content='Se eu jogar uim dado honesto 1000 vezes, qual é a probabilidade de eu obter 150 vezes o número 6? resolva com um código'
)

#rodar a thread no assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions='O nome do usuário é Jefferson Luís e ele é umm usuário premium'
)

#aguardar a thread ser finalizada
while run.status in ['queued', 'in_progress', 'cancelling']:
  time.sleep(1)
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )
  
#verificar a resposta
if run.status == 'completed':
  mensagens = client.beta.threads.messages.list(
    thread_id=thread.id,
  )
  # print(mensagens)
  print(mensagens.data[0].content[0].text.value)
else:
  print('Error', run.status)
  
  
#analisando os passos do modelo
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

for step in run_steps.data[::-1]:
  type_step = step.step_details.type
  print('=== Step', type_step)
  if type_step == 'tool_calls':
    for tool_call in step.step_details.tool_calls:
      print('----')
      print(tool_call.code_interpreter.input)
      print('----')
      print(tool_call.code_interpreter.outputs)
  if type_step == 'message_creation':
    message = client.beta.threads.messages.retrieve(
      thread_id=thread.id,
      message_id=step.step_details.message_creation.message_id
    )
    print(message.content[0].text.value)