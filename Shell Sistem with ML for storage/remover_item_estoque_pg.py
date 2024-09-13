import json, sys
from PyQt6.QtWidgets import (QWidget, QApplication,QLineEdit,
QPushButton, QComboBox, QVBoxLayout, QMessageBox, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Remover_item_estoque(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.setMinimumWidth(100)
		self.setMinimumHeight(100)
		self.setWindowTitle('Remover item')
		self.estoque = {}
		self.historico_vendas = {}
		self.carregar_estoque()
		self.carregar_historico_vendas()
		self.setUpMainWindow()
		self.move(320, 130)
		self.show()
		
	def setUpMainWindow(self):
		self.ed_style = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		estilo_botao = '''
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 4px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		'''
		
		self.pesquisa_item = QLineEdit()
		self.pesquisa_item.setPlaceholderText('Del. Items')
		self.pesquisa_item.textEdited.connect(self.itens_combo)
		self.pesquisa_item.setStyleSheet(self.ed_style)
		
		self.item_combo = QComboBox()
		self.item_combo.setStyleSheet(self.ed_style)
		self.itens_combo()
		
		self.remover_bt = QPushButton('Remover')
		self.remover_bt.setStyleSheet(estilo_botao)
		self.remover_bt.clicked.connect(self.remover)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.pesquisa_item)
		main_v_box.addWidget(self.item_combo)
		main_v_box.addWidget(self.remover_bt)
		self.setLayout(main_v_box)
		
	def itens_combo(self):
		itens = []
		self.item_combo.clear()
		
		if self.pesquisa_item == '':
			self.item_combo.addItems(list(self.estoque.keys()))
		else:
			
			for item, info in self.estoque.items():
				if self.pesquisa_item.text() in item:
					itens.append(item)
					
			self.item_combo.addItems(itens)
					
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
			print('Histórico de vendas não encontrado')		
		
	def salvar_json(self):
		try:
			with open('base_data/estoque.json', 'w') as file:
				json.dump(self.estoque, file)
		except (FileNotFoundError):
			print('Problema com pasta estoque.json')

	def remover(self):
		lista_itens_vendidos = []
		item = self.item_combo.currentText()
		
		
#		for codigo, value in self.historico_vendas.items():
#			for item_, info_item in value['itens'].items():
#				if item_ not in lista_itens_vendidos:
#					lista_itens_vendidos.append(item_)
#				if item_ in lista_itens_vendidos:
#					pass

		#if item not in lista_itens_vendidos:
		answer = QMessageBox.warning(self, 'Excluir item',
		f'''<p>Excluir o item: {item} !?</p>''',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.No)
		if answer == QMessageBox.StandardButton.Yes:
			del self.estoque[item]
			self.item_combo.clear()
			self.item_combo.addItems(list(self.estoque))
			self.salvar_json()
			self.itens_combo()
			
		if answer == QMessageBox.StandardButton.No:
			pass

		#if item in lista_itens_vendidos:
		#	QMessageBox.warning(self, 'Não possibilidade de deletar o item',
		#	f'-{item}-   não pode ser deletado pois já foi vendido!!!',
		#	QMessageBox.StandardButton.Ok,
		#	QMessageBox.StandardButton.Ok)
		

