import sys, json
from datetime import datetime

historico_vendas = {}

def diferenca_dias_guardados(item):
	if historico_vendas:
	
		primeira_data = 0
		ultima_data = 0
		data = 0
		for codigo, value in historico_vendas.items():
			data = value['info']['data']
			
			if item in value['itens']:
				if primeira_data == 0:
					primeira_data = data
				
				ultima_data = data
				
				if ultima_data > data:
					ultima_data = data


				
		#Calculando a diferença de dias
		primeira_data_formatada = datetime.strptime(primeira_data, '%d-%m-%y')
		ultima_data_formatada = datetime.strptime(ultima_data, '%d-%m-%y')
	
		diferenca_dias = (ultima_data_formatada - primeira_data_formatada).days + 1
	
		return diferenca_dias  
	else:
		return 0

def diferenca_dias_totais(item):
	if historico_vendas:
	
		primeira_data = None
		ultima_data = datetime.now().strftime('%d-%m-%y')
	
		for codigo, value in historico_vendas.items():
		
			if item in value['itens']:
				data = value['info']['data']
			
				if primeira_data is None:
					primeira_data = data
				
				
		#Calculando a diferença de dias
		primeira_data_formatada = datetime.strptime(primeira_data, '%d-%m-%y')
		ultima_data_formatada = datetime.strptime(ultima_data, '%d-%m-%y')
	
		diferenca_dias = (ultima_data_formatada - primeira_data_formatada).days + 1
		
		return diferenca_dias  
	else: 
		return 0

def carregar_historico_vendas():
	try:
		with open('base_data/historico_vendas.json', 'r') as file:
			content = file.read()
			if content:
				historico_vendas.update(json.loads(content))
	except (FileNotFoundError, json.JSONDecodeError):
		print('Histórico de vendas não encontrado')	



carregar_historico_vendas()


