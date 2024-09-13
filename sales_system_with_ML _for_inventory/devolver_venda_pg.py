import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit, QComboBox,
QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox,
QTextEdit, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Devolver_venda(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.resize(720, 500)
		self.setWindowTitle('Devolução de itens vendidos')
		self.estoque = {}
		self.historico_vendas = {}
		self.item_quantidade = {} # {Item: quantidade devolvida}
		self.carregar_historico_vendas()
		self.carregar_estoque()
		self.setUpMainWindow()
		self.move(200, 155)
		self.show()
		
	def setUpMainWindow(self):
		fonte = 12

		
		self.codigo_venda_ed = QLineEdit()
		self.codigo_venda_ed.setMaximumWidth(160)
		self.codigo_venda_ed.setMinimumWidth(160)
		self.codigo_venda_ed.setMinimumHeight(30)
		self.codigo_venda_ed.setPlaceholderText('Codigo da venda...')
		self.codigo_venda_ed.setFont(QFont('Arial', 12))
		self.codigo_venda_ed.setClearButtonEnabled(True)
		self.codigo_venda_ed.textEdited.connect(self.combo_box_set)
		
		
		codigo_venda_label = QLabel('Código')
		codigo_venda_label.setFont(QFont('Arial', fonte))
		
		
		self.itens_vendidos_combo = QComboBox()
		self.itens_vendidos_combo.setMaximumWidth(650)
		self.itens_vendidos_combo.setMinimumWidth(300)
		self.itens_vendidos_combo.setMinimumHeight(30)
		self.itens_vendidos_combo.currentIndexChanged.connect(self.combo_selecionado_set)
		
		
		itens_vendidos_label = QLabel('Itens vendidos')
		itens_vendidos_label.setFont(QFont('Arial', fonte))
		
		
		quantidade_vendida_label = QLabel('Vendido')
		quantidade_vendida_label.setFont(QFont('Arial', fonte))
		
		self.quantidade_vendida_label = QLabel('---')
		self.quantidade_vendida_label.setFont(QFont('Arial', fonte))
		
		
		self.quantidade_devolvida_ed = QLineEdit()
		self.quantidade_devolvida_ed.setMaximumWidth(50)
		self.quantidade_devolvida_ed.setMinimumHeight(30)
		self.quantidade_devolvida_ed.setFont(QFont('Arial', 12))
		self.quantidade_devolvida_ed.textEdited.connect(self.apenas_num_pont)
		
		quantidade_devolvida_label = QLabel('Quantidade devolvida')
		quantidade_devolvida_label.setFont(QFont('Arial', fonte))
		
		
		self.valor_total_devolvido_label = QLabel('Total Devolvido: R$ ----')
		self.valor_total_devolvido_label.setFont(QFont('Arial', 16))
		
		self.itens_devolvidos_tedit = QTextEdit()
		
		
		self.botao_devolver_item = QPushButton('Devolver item')
		self.botao_devolver_item.setMaximumWidth(100)
		self.botao_devolver_item.setMinimumHeight(30)
		self.botao_devolver_item.clicked.connect(self.devolver_item)
		
		self.botao_devolver = QPushButton('Finalzar Devolução')
		self.botao_devolver.setMinimumHeight(30)
		self.botao_devolver.clicked.connect(self.finalizar_devolucao)
		
		
		self.venda_info_label = QLabel('Informações da venda:    Venda não encontrada')

		
		main_grid = QGridLayout()
		main_grid.addWidget(codigo_venda_label, 0, 0)
		main_grid.addWidget(self.codigo_venda_ed, 1, 0)
		main_grid.addWidget(itens_vendidos_label, 0, 1)
		main_grid.addWidget(self.itens_vendidos_combo, 1, 1)
		main_grid.addWidget(quantidade_vendida_label, 0, 2)
		main_grid.addWidget(self.quantidade_vendida_label, 1, 2)
		main_grid.addWidget(quantidade_devolvida_label, 0, 3)
		main_grid.addWidget(self.quantidade_devolvida_ed, 1, 3)
		main_grid.addWidget(self.botao_devolver_item, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
		main_grid.addWidget(self.itens_devolvidos_tedit, 3, 0, 1, 4)
		main_grid.addWidget(self.valor_total_devolvido_label, 4, 0, 1, 4)
		main_grid.addWidget(self.botao_devolver, 5, 0, 1, 4)
		main_grid.addWidget(self.venda_info_label, 6, 0, 1, 4)
		main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setLayout(main_grid)
		
	def combo_box_set(self):
		self.itens_devolvidos_tedit.clear()
		self.item_quantidade = {}
		self.valor_total_devolvido_label.setText(f'Total Devolvido: R$ ----')
		self.itens_vendidos_combo.clear()
	
		for codigo, valor in self.historico_vendas.items():
			if self.codigo_venda_ed.text() == codigo:
				itens_vendidos = list(valor['itens'].keys())
				self.itens_vendidos_combo.addItems(itens_vendidos)
			else: 
				pass
	
	def combo_selecionado_set(self):
		item_selecionado = self.itens_vendidos_combo.currentText()
		codigo = self.codigo_venda_ed.text()
		
		if item_selecionado != '':
			self.quantidade_vendida_item = self.historico_vendas[codigo]['itens'][item_selecionado]['quantidade']
			self.quantidade_vendida_label.setText(str(self.quantidade_vendida_item))
			data = self.historico_vendas[codigo]['info']['data']
			dia = self.historico_vendas[codigo]['info']['dia']
			mes = self.historico_vendas[codigo]['info']['mes']
			ano = self.historico_vendas[codigo]['info']['ano']
			self.venda_info_label.setText(f'Informações da venda:    Data: {data}     Dia: {dia}     Mês: {mes}     Ano: {ano}')
		else: 
			self.venda_info_label.setText(f'Informações da venda:    Venda não encontrada')
			self.quantidade_vendida_label.setText('---')
		
	def devolver_item(self):
		if self.codigo_venda_ed.text() != '':
			try:
				codigo = self.codigo_venda_ed.text()
				item = self.itens_vendidos_combo.currentText()
				quantidade_devolvida = self.quantidade_devolvida_ed.text()
				quantidade_vendida = self.historico_vendas[codigo]['itens'][item]['quantidade']
				
				if quantidade_devolvida == '':
					quantidade_devolvida = 0
					
				if float(quantidade_devolvida) > float(quantidade_vendida):
					QMessageBox.warning(self, 'Error de quantidade',
					'Quantidade devolvida maior que a quantidade vendida!!!',
					QMessageBox.StandardButton.Ok,
					QMessageBox.StandardButton.Ok)
				
				if float(quantidade_devolvida) <= float(quantidade_vendida):
					self.itens_devolvidos_tedit.clear()
					total_devolvido = 0
					self.item_quantidade[item] = float(quantidade_devolvida)
					
					for item, quantidade_devolvida in self.item_quantidade.items():
						
						valor_vendido = float(self.historico_vendas[codigo]['itens'][item]['valor'])
						total_item =  valor_vendido * quantidade_devolvida
						total_devolvido += total_item
						
						
						self.itens_devolvidos_tedit.append(f'{item}         Quantidade Devolvida:    {quantidade_devolvida}')
					
					self.valor_total_devolvido_label.setText(f'Total Devolvido: R$ {total_devolvido}')
					
					
				print(self.item_quantidade)

			except KeyError:
				QMessageBox.warning(self, 'Item não encontrado',
				'Selecione uma venda que foi feita!!!',
				QMessageBox.StandardButton.Ok,
				QMessageBox.StandardButton.Ok)
			except ValueError:
				QMessageBox.warning(self, 'Quantidade não suportado',
				'O formato da quantidade a ser devolvida não é suportado',
				QMessageBox.StandardButton.Ok,
				QMessageBox.StandardButton.Ok)
					
		if self.codigo_venda_ed.text() == '':
			QMessageBox.warning(self, 'Venda não selecionada',
			'Selecione a venda para devolver algum item',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)

	def finalizar_devolucao(self):
		if self.codigo_venda_ed.text() != '':
			codigo = self.codigo_venda_ed.text()
			if self.item_quantidade:
				
				for item, quantidade_devolvida in self.item_quantidade.items():
					self.historico_vendas[codigo]['itens'][item]['quantidade'] -= float(quantidade_devolvida)
					self.estoque[item]['quantidade'] += float(quantidade_devolvida)
				
				self.salvar_historico_vendas_json()
				self.salvar_estoque_json()
				print('estoque salvo')

				
				QMessageBox.information(self, 'Devolução',
					'''Devolução feita com SUCESSO!!!''',
					QMessageBox.StandardButton.Ok,
					QMessageBox.StandardButton.Ok)
				self.quantidade_devolvida_ed.clear()
				
				self.close()
			else:
				QMessageBox.warning(self, 'Error', 
				'Nenhum item selecionado para devolução!!!',
				QMessageBox.StandardButton.Ok,
				QMessageBox.StandardButton.Ok)
				
		
		if self.codigo_venda_ed.text() == '':
			QMessageBox.warning(self, 'Error',
			'Nenhuma venda selecionada!!!',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
				
	
	def apenas_num_pont(self):
		for char in self.quantidade_devolvida_ed.text():
			if not char.isdigit() and char != '.':
				self.quantidade_devolvida_ed.clear()
			else:
				a=0			
		
	def carregar_estoque(self):
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Estoque não encontrado')	
			
	def salvar_estoque_json(self):
		with open('base_data/estoque.json', 'w') as file:
			json.dump(self.estoque, file)		
			
		
	
	
	def carregar_historico_vendas(self):
		try:
			with open('base_data/historico_vendas.json', 'r') as file:
				content = file.read()
				if content:
					self.historico_vendas.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas não encontrado')	
	
	def salvar_historico_vendas_json(self):
		with open('base_data/historico_vendas.json', 'w') as file:
			json.dump(self.historico_vendas, file)		
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Devolver_venda()
	sys.exit(app.exec())
