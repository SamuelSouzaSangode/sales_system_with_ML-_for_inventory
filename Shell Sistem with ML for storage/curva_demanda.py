from datetime import datetime
import locale
import json
from diferenca_dias_item_venda import diferenca_dias_guardados
import threading


historico_vendas = {}
estoque = {}
demanda = {}


def set_tempo_tedit_curva_venda(hv, e, d):
	

	item_tempo_estoque = {}

	historico_vendas = hv
	estoque = e
	demanda = d
	


	#item_p = self.pesquisa_item_ed.text()
	itens_base = list(estoque.keys())
	item_quantidade_vendida = {}
	item_media_anual = {} #Item: media_diaria


	for codigo, value in historico_vendas.items():
		for item, info_item in value['itens'].items():
			quantidade_item = info_item['quantidade']
			if item not in item_quantidade_vendida:
				if item in itens_base:
					item_quantidade_vendida[item] = 0
					
			if item in item_quantidade_vendida:
				item_quantidade_vendida[item] += quantidade_item
		

		#Constroi a média entre os dados adquiridos e os gerado de vendas anual
		for item, info_item in estoque.items():
			#Se o item foi vendido e está na curva de demanda
			if item in item_quantidade_vendida and item in demanda:
				media_1 = (float(item_quantidade_vendida[item]) + float(demanda[item])) / (diferenca_dias_guardados(item) + 365)
				resultado_1 = media_1 * 365
				resultado_1_form = round(resultado_1, 1)
				item_media_anual[item] = resultado_1_form
		#Seo o item não foi vendido mas está na curva de demanda
			if item not in item_quantidade_vendida and item in demanda:
				media_2 = float(demanda[item])
				resultado_2_form = round(media_2, 1)
				item_media_anual[item] = resultado_2_form
			#Se o item foi vendido mas não está na curva de demanda	
			if item in item_quantidade_vendida and item not in demanda:
				media_3 = (float(item_quantidade_vendida[item]) / diferenca_dias_guardados(item))
				resultado_3 = media_3 * 365
				resultado_3_form = round(resultado_3, 1)
				item_media_anual[item] = resultado_3_form
			if item not in item_quantidade_vendida and item not in demanda:
				item_media_anual[item] = 0

	#Calculando o tempo de estoque
	for item, info_item in estoque.items():
		try:
			quantidade_estoque = estoque[item]['quantidade']
			
			tempo_estoque = quantidade_estoque / item_media_anual[item]
			tempo_estoque_form = round(tempo_estoque, 2)
				
			item_tempo_estoque[item] = tempo_estoque_form
				
	
		except KeyError:
		
			pass
					
		except ZeroDivisionError:
			pass
	salvar_tempo_media_item(item_tempo_estoque, item_media_anual)
	
	print(item_tempo_estoque)
	print(item_media_anual)




def carregar_json():
	try:
		with open('base_data/estoque.json', 'r') as file:
			content = file.read()
			if content:
				estoque.update(json.loads(content))
				
		with open('base_data/historico_vendas.json', 'r') as file:
			content1 = file.read()
			if content1:
				historico_vendas.update(json.loads(content1))
				
		with open('base_data/demanda.json', 'r') as file:
			content2 = file.read()
			if content2:
				demanda.update(json.loads(content2))
	
	
	
	
	
	except (FileNotFoundError, json.JSONDecodeError):
		pass
		

def salvar_tempo_media_item(item_tempo_estoque, item_media_anual):
	tempo_estoque = item_tempo_estoque
	media_anual = item_media_anual
	a = datetime.now().strftime('%d-%m-%y')
	try:
		with open('base_data/item_tempo_estoque.json', 'w') as file:
			json.dump(tempo_estoque, file)
	
		with open('base_data/item_media_anual.json', 'w') as file:
			json.dump(media_anual, file)
		
		with open('base_data/ultima_atualizacao_data.txt', 'w') as file:	
			file.write(a)
		
	except FileNotFoundError:
		pass
		




def item_t_e_item_media_anual():

	carregar_json()
	thread = threading.Thread(target=set_tempo_tedit_curva_venda, args=(historico_vendas,estoque,demanda))
	thread.start()
	







