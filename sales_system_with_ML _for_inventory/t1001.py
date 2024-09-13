import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
QLineEdit, QTextEdit, QCheckBox, QComboBox, QGridLayout, QFrame, 
QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from t1001settings import T1001_configuracoes
from diferenca_dias_item_venda import diferenca_dias_guardados
from collections import OrderedDict
from datetime import datetime

class T1001(QWidget):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.resize(700, 700)
		self.setWindowTitle('T1001 Adm')
		self.estoque = {}
		self.historico_vendas = {}
		self.config = {}
		self.demanda = {}
		self.item_tempo_estoque = {}
		self.item_media_anual = {}
		self.carregar_historico_vendas()
		self.carregar_estoque()
		self.setUpMainWindow()
		self.showMaximized()
		
	def setUpMainWindow(self):
#####FINACEIRO E ESTOQUE################################################
		estilo_botao_t1001 = """
			QPushButton {background-color: #353535;
			color: red;
			border-radius: 10px;
			border: none;}
			
		QPushButton:pressed {background-color: #FFFFFF;}
			"""
		ed_estilo = '''
		border-radius: 10px; border: 2px solid gray'''
		estilo_botao = """
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""		
		
		botao_atualizar = QPushButton('Atualizar')
		botao_atualizar.clicked.connect(self.set)
		
		
		t1001_botao = QPushButton('T1001 - Pro')
		t1001_botao.setStyleSheet(estilo_botao_t1001)
		t1001_botao.setFont(QFont('Arial', 22))
		t1001_botao.clicked.connect(self.configuracoes)
		
		self.precisao_label = QLabel('Precisão: 98%')
		self.precisao_label.setFont(QFont('Arial', 10))
		
		self.data = QLabel('Data: 30/11/2023')
		self.data.setFont(QFont('Arial', 16))
		
		financeiro_label = QLabel('Financeiro:')
		financeiro_label.setFont(QFont('Arial', 18))
		
		self.faturado_hoje_label = QLabel('Faturado Hoje:  R$------')
		self.faturado_hoje_label.setFont(QFont('Arial', 12))
		
		self.lucro_hoje_label = QLabel('Lucro Hoje:  R$------')
		self.lucro_hoje_label.setFont(QFont('Arial', 12))
		
		self.faturamento_mes_atual_label = QLabel('Faturado Mês:  R$-----')
		self.faturamento_mes_atual_label.setFont(QFont('Arial', 12))
		
		self.lucro_mes_atual_label = QLabel('Lucro Mês:  R$-----')
		self.lucro_mes_atual_label.setFont(QFont('Arial', 12))
		
		self.ultima_data_atualizacao = QLabel('Data Att: ++-++-++')
		self.ultima_data_atualizacao.setFont(QFont('Arial', 12))
		
		linha = QFrame()
		linha.setFrameShape(QFrame.Shape.HLine)  # Define o tipo de linha como horizontal
		linha.setFrameShadow(QFrame.Shadow.Sunken)  # Define a sombra da linha
		
		estoque_label = QLabel('Estoque:')
		estoque_label.setFont(QFont('Arial',18))
		
		self.valor_estoque_label = QLabel('Estoque Atual: R$ ------')
		self.valor_estoque_label.setFont(QFont('Arial', 12))
		
		self.nivel_estoque_label = QLabel('Nível de estoque: ++++++++++#')
		self.nivel_estoque_label.setFont(QFont('Arial', 12))
		
		self.estoque_manutencao_label = QLabel('Manutenção: R$----')
		self.estoque_manutencao_label.setFont(QFont('Arial', 12))
		
		self.tempo_estoque_geral_label = QLabel('Tempo Geral: ---- anos')
		self.tempo_estoque_geral_label.setFont(QFont('Aria', 12))

		linha_2 = QFrame()
		linha_2.setFrameShape(QFrame.Shape.HLine)  # Define o tipo de linha como horizontal
		linha_2.setFrameShadow(QFrame.Shadow.Sunken)  # Define a sombra da linha		
#####TEMPO DE ESTOQUE###################################################
		tempo_estoque_1_label = QLabel('Tempo de estoque')
		tempo_estoque_1_label.setFont(QFont('Arial', 16))
		
		self.pesquisa_item_ed = QLineEdit()
		self.pesquisa_item_ed.setPlaceholderText('Item ou vários itens...')
		self.pesquisa_item_ed.setFixedHeight(35)
		self.pesquisa_item_ed.setFont(QFont('Arial', 12))
		self.pesquisa_item_ed.setStyleSheet(ed_estilo)
		self.pesquisa_item_ed.setClearButtonEnabled(True)
		self.pesquisa_item_ed.textEdited.connect(self.pesquisa_item_tempo)
		
		self.tempo_orcamento_ed = QLineEdit('1')
		self.tempo_orcamento_ed.setPlaceholderText('Tempo...')
		self.tempo_orcamento_ed.setStyleSheet(ed_estilo)
		self.tempo_orcamento_ed.setClearButtonEnabled(True)
		self.tempo_orcamento_ed.setFixedWidth(100)
		
		self.tempo_estoque_pesquisa_tabela = QTableWidget()
		self.tempo_estoque_pesquisa_tabela.setStyleSheet(ed_estilo)
		self.tempo_estoque_pesquisa_tabela.setFont(QFont('Time New Roman', 8))

		
		
		tempo_estoque_2_label = QLabel('Consumo de estoque por tempo')
		tempo_estoque_2_label.setFont(QFont('Arial', 16))
		
		self.tempo_estoque_portempo_tabela = QTableWidget()
		self.tempo_estoque_portempo_tabela.setFont(QFont('Arial', 12))
		self.tempo_estoque_portempo_tabela.setStyleSheet(ed_estilo)
		
		self.data_inicial = QLineEdit()
		self.data_inicial.setFixedSize(120, 35)
		self.data_inicial.setStyleSheet(ed_estilo)
		self.data_inicial.setPlaceholderText('dd-mm-yy Inicial')
		
		self.data_final = QLineEdit()
		self.data_final.setFixedSize(120, 35)
		self.data_final.setStyleSheet(ed_estilo)
		self.data_final.setPlaceholderText('dd-mm-yy Final')
		
		calcular_portempo_botao = QPushButton('Calcular')
		calcular_portempo_botao.setFont(QFont('Arial', 12))
		calcular_portempo_botao.setStyleSheet(estilo_botao)
		calcular_portempo_botao.clicked.connect(self.set_itens_consumidos)
		
		self.consumo_label = QLabel('Consumo:  R$ -----')
		self.consumo_label.setFont(QFont('Arial', 12))
		
		self.faturado_label = QLabel('Faturado: R$ -----')
		self.faturado_label.setFont(QFont('Arial', 12))
		
		
		main_grid = QGridLayout()
		main_grid.addWidget(t1001_botao, 0, 0)
		main_grid.addWidget(self.precisao_label, 0, 1)
		main_grid.addWidget(self.data, 0, 9)
		main_grid.addWidget(financeiro_label, 1, 0)
		main_grid.addWidget(self.faturado_hoje_label, 2, 0, 1, 2)
		main_grid.addWidget(self.lucro_hoje_label, 2, 3, 1, 3)
		main_grid.addWidget(self.faturamento_mes_atual_label, 2, 6, 1, 3)
		main_grid.addWidget(self.ultima_data_atualizacao, 0, 6)
		main_grid.addWidget(self.lucro_mes_atual_label, 2, 9)
		main_grid.addWidget(linha, 3, 0, 1, 10)
		main_grid.addWidget(estoque_label, 4, 0)
		main_grid.addWidget(self.valor_estoque_label, 5, 0, 1, 2)
		main_grid.addWidget(self.nivel_estoque_label, 5, 3, 1, 3)
		main_grid.addWidget(self.estoque_manutencao_label, 5, 6, 1, 3)
		main_grid.addWidget(self.tempo_estoque_geral_label, 5, 9)
		main_grid.addWidget(linha_2, 6, 0, 1, 10)
##Tempo estoque
		main_grid.addWidget(tempo_estoque_1_label, 7, 0)
		main_grid.addWidget(self.pesquisa_item_ed, 8, 0, 1, 2)
		main_grid.addWidget(self.tempo_orcamento_ed, 9, 0, 1, 1)
		main_grid.addWidget(self.tempo_estoque_pesquisa_tabela, 10, 0, 1, 7)
		main_grid.addWidget(tempo_estoque_2_label, 7, 7, 1, 2)
		main_grid.addWidget(self.data_inicial, 8, 7, 1, 1)
		main_grid.addWidget(self.data_final, 8, 9, 1, 1)
		main_grid.addWidget(calcular_portempo_botao, 9, 7, 1, 3)
		main_grid.addWidget(self.tempo_estoque_portempo_tabela, 10, 7, 1, 3)
		main_grid.addWidget(self.consumo_label, 11, 7, 1, 1)
		main_grid.addWidget(self.faturado_label, 11, 9, 1, 1)
		main_grid.addWidget(botao_atualizar, 11, 0, 1, 1)

		main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setLayout(main_grid)
		
		self.set()
		
	def faturado_hoje(self):
		faturado_hoje = 0
		data_hoje = datetime.now().strftime('%d-%m-%y')
		for codigo, value in self.historico_vendas.items():
			if data_hoje == value['info']['data']:
				for item, info_item in value['itens'].items():
					total_vendido_item = info_item['quantidade'] * info_item['valor']
					faturado_hoje += total_vendido_item
				faturado_hoje_form = round(faturado_hoje, 2)
				self.faturado_hoje_label.setText(f'Faturado Hoje:  R${str(faturado_hoje_form)}')
				
		if faturado_hoje == 0:
			self.faturado_hoje_label.setText('Faturado Hoje:  R$------')

	def faturado_mes(self):
		faturado_mes = 0
		data_hoje = datetime.now().strftime('%m-%y')
		for codigo, value in self.historico_vendas.items():
			if data_hoje == value['info']['mes_ano']:
				for item, info_item in value['itens'].items():
					total_vendido_item = info_item['quantidade'] * info_item['valor']
					faturado_mes += total_vendido_item
				faturado_mes_form = round(faturado_mes, 2)
				self.faturamento_mes_atual_label.setText(f'Faturado Mês:  R${str(faturado_mes_form)}')
				
		if faturado_mes == 0:
			self.faturamento_mes_atual_label.setText('Faturado Mês:  R$------')
			
	def lucro_hoje(self):
		faturado_hoje = 0
		custo_hoje = 0
		lucro_hoje = 0
		
		data_hoje = datetime.now().strftime('%d-%m-%y')
		for codigo, value in self.historico_vendas.items():
			if data_hoje == value['info']['data']:
				for item, info_item in value['itens'].items():
					total_vendido_item = info_item['quantidade'] * info_item['valor']
					faturado_hoje += total_vendido_item
				
				for item, info_item in value['itens'].items():
					custo_total_item = info_item['quantidade'] * info_item['custo']
					custo_hoje += custo_total_item
				
				resultado = faturado_hoje - custo_hoje
				lucro_hoje_form = round(resultado, 2)
				self.lucro_hoje_label.setText(f'Lucro Hoje: R${str(lucro_hoje_form)}')
				
				
				
			
			
			if faturado_hoje == 0:
				self.lucro_hoje_label.setText('Lucro Hoje:  R$------')
		
	def lucro_mes(self):
		faturado_mes = 0
		custo_mes = 0
		lucro_mes = 0
		
		data_hoje = datetime.now().strftime('%m-%y')
		for codigo, value in self.historico_vendas.items():
			if data_hoje == value['info']['mes_ano']:
				for item, info_item in value['itens'].items():
					total_vendido_item = info_item['quantidade'] * info_item['valor']
					faturado_mes += total_vendido_item
				
				for item, info_item in value['itens'].items():
					custo_total_item = info_item['quantidade'] * info_item['custo']
					custo_mes += custo_total_item
				
				resultado = faturado_mes - custo_mes
				lucro_mes_form = round(resultado, 2)
				self.lucro_mes_atual_label.setText(f'Lucro Mês: R${str(lucro_mes_form)}')
				
				
				
			
			
			if faturado_mes == 0:
				self.lucro_mes_atual_label.setText('Lucro Mês:  R$------')
	
	def valor_estoque(self):
		icms = self.config['icms']
		valor_estoque = 0
		for item, info_item in self.estoque.items():
			total_item = info_item['quantidade'] * info_item['custo']
			valor_estoque += total_item
		valor_estoque_icms = (valor_estoque * icms) + valor_estoque
		self.valor_estoque_label.setText(f'Estoque Atual: R$ {round(valor_estoque_icms, 2)}')
		
	def nivel_estoque(self):
		estoque_maximo = self.config['estoque_maximo']
		estoque_minimo = self.config['estoque_minimo']
		valor_estoque = 0
		
		for item, info_item in self.estoque.items():
			total_item = info_item['quantidade'] * info_item['custo']
			valor_estoque += total_item
		
		valor_estoque_icms = (valor_estoque * 0.18) + valor_estoque
		#valor_estoque_icms = 110000
		
		diferenca = float(estoque_maximo) - float(estoque_minimo)
		partes = diferenca / 10
		parte_1 = partes * 1
		parte_2 = partes * 2
		parte_3 = partes * 3
		parte_4 = partes * 4
		parte_5 = partes * 5
		parte_6 = partes * 6
		parte_7 = partes * 7
		parte_8 = partes * 8
		parte_9 = partes * 9
		parte_10 = partes * 10
		
		diferenca_atual = float(valor_estoque_icms) - float(estoque_minimo)
		
		if valor_estoque_icms <= estoque_minimo:
			self.nivel_estoque_label.setText('Nível de estoque: Hora de repor')
			
		
		if diferenca_atual >= parte_1:


			self.nivel_estoque_label.setText('Nível de estoque: +')

		if diferenca_atual >= parte_2:


			self.nivel_estoque_label.setText('Nível de estoque: ++')

		if diferenca_atual >= parte_3:


			self.nivel_estoque_label.setText('Nível de estoque: +++')

		if diferenca_atual >= parte_4:


			self.nivel_estoque_label.setText('Nível de estoque: ++++')
			
		if diferenca_atual >= parte_5:


			self.nivel_estoque_label.setText('Nível de estoque: +++++')
			
		if diferenca_atual >= parte_6:

			self.nivel_estoque_label.setText('Nível de estoque: ++++++')
		
		if diferenca_atual >= parte_7:


			self.nivel_estoque_label.setText('Nível de estoque: +++++++')	

		if diferenca_atual >= parte_8:


			self.nivel_estoque_label.setText('Nível de estoque: ++++++++')

		if diferenca_atual >= parte_9:


			self.nivel_estoque_label.setText('Nível de estoque: ++++++++++')
			
		if diferenca_atual >= parte_10:


			self.nivel_estoque_label.setText('Nível de estoque: ++++++++++#')

	def manutencao(self):
		icms = self.config['icms']
		estoque_maximo = self.config['estoque_maximo']
		valor_estoque = 0
		for item, info_item in self.estoque.items():
			total_item = info_item['quantidade'] * info_item['custo']
			valor_estoque += total_item
		valor_estoque_icms = (valor_estoque * icms) + valor_estoque
		
		resultado = valor_estoque_icms - estoque_maximo
		resultado_form = round(resultado, 2)
		self.estoque_manutencao_label.setText(f'Manutenção: R$ {resultado_form}')
		
	def tempo_geral(self):
		consumo_estoque_anual = self.config['estoque_anual']
		valor_estoque = 0
		for item, info_item in self.estoque.items():
			total_item = info_item['quantidade'] * info_item['custo']
			valor_estoque += total_item
		
		resultado = valor_estoque / consumo_estoque_anual
		resultado_form = round(resultado, 2)
		self.tempo_estoque_geral_label.setText(f'Tempo Geral: {resultado_form} anos')
		
	def data_atual(self):
		data_atual = datetime.now().strftime('%d-%m-%y')
		self.data.setText(f'Data: {data_atual}')
		
	def data_ultima_atualizacao(self):
		data_str = ''
		try:
			with open('base_data/ultima_atualizacao_data.txt', 'r') as arquivo:
				data_str = arquivo.read()
				if data_str:
					self.ultima_data_atualizacao.setText(f'Data Att: {data_str}')
				else:
					self.ultima_data_atualizacao.setText('Data Att: ++-++-++')
		
		
		except:
			pass
		
		
			
	def set_tempo_tedit_curva_venda(self):
		self.carregar_tempo_media()


	
	def pesquisa_item_tempo(self):
		self.tempo_estoque_pesquisa_tabela.clear()
		item_p = self.pesquisa_item_ed.text()
		itens_ordenados = OrderedDict(sorted(self.item_tempo_estoque.items(), key=lambda x: x[1]))
		#Aplica as linhas na tabela de acordo com a quantidae de itens
		self.tempo_estoque_pesquisa_tabela.setRowCount(len(self.item_tempo_estoque))
		self.tempo_estoque_pesquisa_tabela.setColumnCount(4)
		self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
			0, QTableWidgetItem('Anos Disp'))
			
		self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
			1, QTableWidgetItem('Produto'))
				
		self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
			2, QTableWidgetItem('Compra'))
			
		self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
			3, QTableWidgetItem('Estoque'))	
	
		
		if self.pesquisa_item_ed.text() != '':
			itens_ordenados =  items_ordenados = OrderedDict(sorted(self.item_tempo_estoque.items(), key=lambda x: x[1]))	
			var_linha = 0
			for item, tempo in itens_ordenados.items():
				if self.pesquisa_item_ed.text() in item:
					try:
						quantidade = (self.item_media_anual[item] * float(self.tempo_orcamento_ed.text()))
						quantidade_form = round(quantidade, 2)
					except:
						quantidade = self.item_media_anual[item]
						quantidade_form = quantidade
					
					self.tempo_estoque_pesquisa_tabela.setItem(
						var_linha, 0, QTableWidgetItem(f'{tempo} anos'))
						
					self.tempo_estoque_pesquisa_tabela.setItem(
						var_linha,2, QTableWidgetItem(
						f'{quantidade_form} para ({self.tempo_orcamento_ed.text()}) anos'))

					self.tempo_estoque_pesquisa_tabela.setItem(
						var_linha, 3, QTableWidgetItem( f" Qnt: {str(self.estoque[item]['quantidade'])}" ))
					
					self.tempo_estoque_pesquisa_tabela.setItem(
						var_linha, 1, QTableWidgetItem(item))
					var_linha += 1
				
		if self.pesquisa_item_ed.text() == '':	
			self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
				0, QTableWidgetItem('Anos Disp'))
			
			self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
				1, QTableWidgetItem('Produto'))
				
			self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
				2, QTableWidgetItem('Compra'))
			
			self.tempo_estoque_pesquisa_tabela.setHorizontalHeaderItem(
				3, QTableWidgetItem('Estoque'))		
			
			var_linha1 = 0
			
			for item1, tempo1 in itens_ordenados.items():
				try:
					quantidade = (self.item_media_anual[item1] * float(self.tempo_orcamento_ed.text()))
					quantidade_form = round(quantidade, 2)
				except:
					quantidade = self.item_media_anual[item1]
					quantidade_form = quantidade
				self.tempo_estoque_pesquisa_tabela.setItem(
					var_linha1, 0, QTableWidgetItem(f'{tempo1} anos'))	
				self.tempo_estoque_pesquisa_tabela.setItem(
					var_linha1, 2, QTableWidgetItem(
					f'{quantidade_form} para ({self.tempo_orcamento_ed.text()}) anos'))
					
				self.tempo_estoque_pesquisa_tabela.setItem(
					var_linha1, 1, QTableWidgetItem(item1))
					
				self.tempo_estoque_pesquisa_tabela.setItem(
					var_linha1, 3, QTableWidgetItem( f" Qnt: {str(self.estoque[item1]['quantidade'])}" ))
				
				var_linha1 += 1		
		self.tempo_estoque_pesquisa_tabela.resizeColumnsToContents()		
	
	def set_itens_consumidos(self):
		try:
			
			#Itens vendidos apenas no período
			itens_vendidos = {}
			
			data_inicial = datetime.strptime(self.data_inicial.text(), '%d-%m-%y')
			data_final = datetime.strptime(self.data_final.text(), '%d-%m-%y')

			custo = 0
			valor = 0
		
		
			for codigo, value in self.historico_vendas.items():
				data = datetime.strptime(value['info']['data'], '%d-%m-%y')
			
			
				if data >= data_inicial and data <= data_final:

			
					for item, info in value['itens'].items():
						quantidade_item = info['quantidade']
						custo_item = info['custo']
						custo_total_item = quantidade_item * custo_item
						custo += custo_total_item
					
						valor_venda = info['valor']
						valor_total_item = quantidade_item * valor_venda
						valor += valor_total_item
					
					
					
						if item in itens_vendidos:
							itens_vendidos[item] += info['quantidade']
					
						if item not in itens_vendidos:
							itens_vendidos[item] = info['quantidade']
					
					
		
			itens_ordenados = OrderedDict(sorted(itens_vendidos.items(), key=lambda x: x[1]))			
			self.tempo_estoque_portempo_tabela.setRowCount(len(list(itens_vendidos.keys())))
			self.tempo_estoque_portempo_tabela.setColumnCount(2)			
			
			var_linha = 0
			for item, quantidade in itens_ordenados.items():
				self.tempo_estoque_portempo_tabela.setItem(
					var_linha, 0, QTableWidgetItem(item))
					
				self.tempo_estoque_portempo_tabela.setItem(
					var_linha, 1, QTableWidgetItem(f'{quantidade} unidades'))
				var_linha += 1	
			
			custo_form = round(custo, 2)
			self.consumo_label.setText(f'Consumo: R$ {str(custo_form)}')
		
			valor_form = round(valor, 2)
			self.faturado_label.setText(f'Faturado: R$ {str(valor_form)}')
			self.tempo_estoque_portempo_tabela.resizeColumnsToContents()
		except:
			print('Error na data de cosumos')

	def set(self):
		
		try:
			self.carregar_json()
		except :
			pass
		
		try:
			self.carregar_estoque()
		except :
			pass
		
		try:
			self.carregar_historico_vendas()
		except :
			pass
		
		try:
			self.carregar_demanda()
		except :
			pass
		
		try:
			self.set_tempo_tedit_curva_venda()
		except :
			pass
		
		try:
			self.pesquisa_item_tempo()
		except :
			pass
		try:
			self.faturado_hoje()	
		except :
			pass
		
		try:
			self.lucro_hoje()
		except :
			pass
		try:	
			self.faturado_mes()
		except :
			pass
			
		try:
			self.lucro_mes()
		except :
			pass
			
		try:
			self.valor_estoque()
		except :
			pass
		
		try:
			self.nivel_estoque()
		except :
			pass
		
		try:
			self.manutencao()
		except :
			pass
		try:
			self.tempo_geral()
		except :
			pass
		try:	
			self.data_atual()
		except :
			pass
		try:
			self.data_ultima_atualizacao()
		except:
			pass
			
	def configuracoes(self):
		self.window = T1001_configuracoes()
		self.window.show()
			
	def carregar_estoque(self):
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu estoque')	
			
	def carregar_historico_vendas(self):
		try:
			with open('base_data/historico_vendas.json', 'r') as file:
				content = file.read()
				if content:
					self.historico_vendas.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas não encontrados')	

	def carregar_json(self):
		try:
			with open('base_data/config.json', 'r') as file:
				content = file.read()
				if content:
					self.config.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			pass

	def carregar_demanda(self):
		try:
			with open('base_data/demanda.json', 'r') as file:
				content = file.read()
				if content:
					self.demanda.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Demanda não encontrada')	
	
	def carregar_tempo_media(self):
		try:
			with open('base_data/item_tempo_estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.item_tempo_estoque.update(json.loads(content))
				
			with open('base_data/item_media_anual.json', 'r') as file:
				content2 = file.read()
				if content2:
					self.item_media_anual.update(json.loads(content2))
		
		
		
		except (FileNotFoundError, json.JSONDecodeError):
			pass
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = T1001()
	sys.exit(app.exec())

