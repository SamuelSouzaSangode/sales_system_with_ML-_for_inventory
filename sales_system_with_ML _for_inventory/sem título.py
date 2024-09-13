import json
demanda = {}

def carregar_demanda():
	try:
		with open('base_data/demanda.json', 'r') as file:
			content = file.read()
			if content:
				demanda.update(json.loads(content))
	except (FileNotFoundError, json.JSONDecodeError):
		print('Demanda não encontrada')	

carregar_demanda()
for item, demanda in demanda.items():
	if 'phi' in item:
		print(f'{item} {demanda}')
