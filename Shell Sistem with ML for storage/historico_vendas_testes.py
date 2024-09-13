import json, sys
from PyQt6.QtWidgets import QWidget, QApplication, QLineEdit, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from diferenca_dias_item_venda import diferenca_dias_totais
from diferenca_dias_item_venda import diferenca_dias_guardados

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.resize(600, 600)
		self.setWindowTitle('Testes edit historico de vendas')
		self.demanda = {}
		self.estoque = {}
		self.historico_vendas = {}
		self.carregar_demanda()
		self.carregar_estoque()
		self.carregar_historico_vendas()
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		self.tempo_estoque_ed = QLineEdit('1')
		self.tempo_estoque_ed.setPlaceholderText('Tempo de estoque')
		self.tempo_estoque_ed.resize(60, 30)
		self.tempo_estoque_ed.textEdited.connect(self.set_tempo_tedit_curva_venda)
		
		
		self.itens_tempo_estoque_td = QTextEdit()
		self.itens_tempo_estoque_td.resize(300, 400)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.tempo_estoque_ed)
		main_v_box.addWidget(self.itens_tempo_estoque_td)
		self.setLayout(main_v_box)
		
		self.set_tempo_tedit_curva_venda()
	
	#Apenas venda
	def set_tempo_tedit_venda(self):
		item_quantidade_vendida = {}
		item_media_diaria = {}
		
		#Adiciona os itens vendidos com as quantidades vendidas no dicionário
		#Então esse dicionário so tem itens que foram vendidos
		for codigo, value in self.historico_vendas.items():
			for item, info_item in value['itens'].items():
				quantidade = info_item['quantidade']
				#Se o item já foi vendido --- será somado
				if item in item_quantidade_vendida:
					item_quantidade_vendida[item] += quantidade
				#Se ainda não foi vendido --- será adicionado
				if item not in item_quantidade_vendida:
					item_quantidade_vendida[item] = quantidade
		
		#Constroi a média entre os dados adquiridos e os gerado de vendas anual
		for item, info_item in self.estoque.items():
			if item in item_quantidade_vendida:
				media_1 = (float(item_quantidade_vendida[item]) / diferenca_dias_guardados(item))
				resultado_1= media_1 * 365
				resultado_1_form = round(resultado_1, 1)
				item_media_diaria[item] = resultado_1_form
				

				
				
		#Calculando o tempo de estoque
		for item, info_item in self.estoque.items():
			try:
				quantidade_estoque = self.estoque[item]['quantidade']
			
				tempo_estoque = quantidade_estoque / item_media_diaria[item]
				tempo_estoque_form = round(tempo_estoque, 2)
				self.itens_tempo_estoque_td.append(f'Anos: {tempo_estoque_form}       {item}')
				
			except KeyError:
				self.itens_tempo_estoque_td.append(f'Anos: --       {item}')
					
			except ZeroDivisionError:
				self.itens_tempo_estoque_td.append(f'Anos: 0       {item}')
			
				
		print(item_quantidade_vendida)
		print(item_media_diaria)
	
	#Venda e os dados da curva
	def set_tempo_tedit_curva_venda(self):
		try:
			item_quantidade_vendida = {}
			item_media_diaria = {}
		
			#Adiciona os itens vendidos com as quantidades vendidas no dicionário
			#Então esse dicionário so tem itens que foram vendidos
			for codigo, value in self.historico_vendas.items():
				for item, info_item in value['itens'].items():
					quantidade = info_item['quantidade']
					#Se o item já foi vendido --- será somado
					if item in item_quantidade_vendida:
						item_quantidade_vendida[item] += quantidade
					#Se ainda não foi vendido --- será adicionado
					if item not in item_quantidade_vendida:
						item_quantidade_vendida[item] = quantidade
		
			#Constroi a média entre os dados adquiridos e os gerado de vendas anual
			for item, info_item in self.estoque.items():
				#Se o item foi vendido e está na curva de demanda
				if item in item_quantidade_vendida and item in self.demanda:
					media_1 = (float(item_quantidade_vendida[item]) + float(self.demanda[item])) / (diferenca_dias_guardados(item) + 365)
					resultado_1 = media_1 * 365
					resultado_1_form = round(resultado_1, 1)
					item_media_diaria[item] = resultado_1_form
			#Seo o item não foi vendido mas está na curva de demanda
				if item not in item_quantidade_vendida and item in self.demanda:
					media_2 = float(self.demanda[item])
					resultado_2_form = round(media_2, 1)
					item_media_diaria[item] = resultado_2_form
				#Se o item foi vendido mas não está na curva de demanda	
				if item in item_quantidade_vendida and item not in self.demanda:
					media_3 = (float(item_quantidade_vendida[item]) / diferenca_dias_guardados(item))
					resultado_3 = media_3 * 365
					resultado_3_form = round(resultado_3, 1)
					item_media_diaria[item] = resultado_3_form
				

				

				
				
			#Calculando o tempo de estoque
			for item, info_item in self.estoque.items():
				try:
					quantidade_estoque = self.estoque[item]['quantidade']
			
					tempo_estoque = quantidade_estoque / item_media_diaria[item]
					tempo_estoque_form = round(tempo_estoque, 2)
				
					if tempo_estoque <= float(self.tempo_estoque_ed.text()):
						self.itens_tempo_estoque_td.append(f'Anos: {tempo_estoque_form}       {item}')

			
				except KeyError:
					pass
				#self.itens_tempo_estoque_td.append(f'Anos: --       {item}')
					
				except ZeroDivisionError:
					pass
				#self.itens_tempo_estoque_td.append(f'Anos: --       {item}')
			
		except ValueError:
			self.itens_tempo_estoque_td.clear()


	
	def carregar_demanda(self):
		try:
			with open('base_data/demanda.json', 'r') as file:
				content = file.read()
				if content:
					self.demanda.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas não encontrado')		


	def carregar_estoque(self):
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas não encontrado')	
			
	def carregar_historico_vendas(self):
		try:
			with open('base_data/historico_vendas.json', 'r') as file:
				content = file.read()
				if content:
					self.historico_vendas.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas não encontrado')	
				

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())
		
	
