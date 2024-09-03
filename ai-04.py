# function callings: o retorno da função sempre é texto
# tools = é a ferramenta que o modelo usa, é nela que fica a função
# tool_choice = o modelo tem a inteligencia de definir que tool usar ou podemos predefinir

import json
import openai
import yfinance as yf
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

def retorna_cotacao_historica(ticker, periodo='1mo'):
  ticker = ticker.rstrip('.SA')
  ticker_obj = yf.Ticker(f'{ticker}.SA')
  hist = ticker_obj.history(period=periodo, auto_adjust=False)
  hist = round(hist, 2)
  if len(hist) > 30:
    slice_size = int(len(hist) / 30)
    hist = hist.iloc[::-slice_size][::-1]
  hist.index = hist.index.strftime('%m-%d-%Y')
  return hist['Close'].to_json()

# response = retorna_cotacao_historica('ABEV3', '5y')
# print(response)

tools = [
  {
    'type': 'function',
    'function': {
      'name': 'retorna_cotacao_historica',
      'description': 'Retorna a cotação histórica para uma ação da bovespa',
      'parameters': {
        'type': 'object',
        'properties': {
          'ticker': {
            'type': 'string',
            'description': 'O ticker da ação. Exemplo: "ABEV3" para ambev, "PETR4" para petrobras, etc'
          },
          'periodo': {
            'type': 'string',
            'description': 'O período que será retornado de dados históricos   \
                            sendo "1mo" equivalente a um mês de dados, "1d" a \
                            1 dia e "1y" a 1 ano',
            'enum': ['1d', '5d', '1mo', '6mo', '1y', '5y', '10y', 'ytd', 'max']
          }
        }
      }
    }
  }
]

funcoes_disponiveis = {
  'retorna_cotacao_historica': retorna_cotacao_historica
}

def gera_texto(mensagens):
  resposta = client.chat.completions.create(
    messages=mensagens, 
    model='gpt-4o-mini', 
    max_tokens=1000, 
    temperature=0, 
    tools=tools, 
    tool_choice='auto'
  )

  tool_calls = resposta.choices[0].message.tool_calls

  if tool_calls:
    mensagens.append(resposta.choices[0].message)
    for tool_call in tool_calls:
      func_name = tool_call.function.name
      func_to_call = funcoes_disponiveis[func_name]
      func_args = json.loads(tool_call.function.arguments)
      func_return = func_to_call(**func_args)
      mensagens.append({
        'tool_call_id': tool_call.id,
        'role': 'tool',
        'name': func_name,
        'content': func_return
      })
      
    segunda_resposta = client.chat.completions.create(
      messages=mensagens,
      model='gpt-4o-mini',
      max_tokens=1000,
      temperature=0,
    )
    
    mensagens.append(segunda_resposta.choices[0].message.model_dump(exclude_none=True))
    
  print(f'Assistant: {mensagens[-1]["content"]}')
  return mensagens


if __name__ == '__main__':
  print('Bem vindo ao Jeff Corretor')
  mensagens = []
  while True:
    input_usuario = input('Usuário: ')
    mensagens.append({'role': 'user', 'content': input_usuario})
    mensagens = gera_texto(mensagens)