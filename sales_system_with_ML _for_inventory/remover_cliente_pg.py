import json, sys
from PyQt6.QtWidgets import (QWidget, QApplication,QLineEdit,
QPushButton, QComboBox, QVBoxLayout, QMessageBox, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Remover_cliente(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.setMinimumWidth(100)
		self.setMinimumHeight(100)
		self.setWindowTitle('Remover cliente')
		self.cliente = {}
		self.carregar_cliente()
		self.setUpMainWindow()
		self.move(320, 160)
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
		
		self.pesquisa_cliente = QLineEdit()
		self.pesquisa_cliente.setPlaceholderText('Del. cliente')
		self.pesquisa_cliente.textEdited.connect(self.clientes_combo)
		self.pesquisa_cliente.setStyleSheet(self.ed_style)
		
		self.cliente_combo = QComboBox()
		self.cliente_combo.setStyleSheet(self.ed_style)
		self.clientes_combo()
		
		self.remover_bt = QPushButton('Remover')
		self.remover_bt.setStyleSheet(estilo_botao)
		self.remover_bt.clicked.connect(self.remover)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.pesquisa_cliente)
		main_v_box.addWidget(self.cliente_combo)
		main_v_box.addWidget(self.remover_bt)
		self.setLayout(main_v_box)
		
	def clientes_combo(self):
		clientes = []
		self.cliente_combo.clear()
		
		if self.pesquisa_cliente == '':
			self.cliente_combo.addItems(list(self.cliente.keys()))
		else:
			
			for cliente, info in self.cliente.items():
				if self.pesquisa_cliente.text() in cliente:
					clientes.append(cliente)
					
			self.cliente_combo.addItems(clientes)
					
		
	def carregar_cliente(self):
		try:
			with open('base_data/cliente.json', 'r') as file:
				content = file.read()
				if content:
					self.cliente.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu fornecedor')
			
	def salvar_json(self):
		try:
			with open('base_data/cliente.json', 'w') as file:
				json.dump(self.cliente, file)
		except (FileNotFoundError):
			print('Problema com pasta estoque.json')

	def remover(self):
		cliente = self.cliente_combo.currentText()
		
		answer = QMessageBox.warning(self, 'Excluir fornecedor',
		f'''<p>Excluir o Cliente: {cliente} !?</p>''',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.No)
		
		if answer == QMessageBox.StandardButton.Yes:
			del self.cliente[cliente]
			self.cliente_combo.clear()
			self.cliente_combo.addItems(list(self.cliente))
			self.salvar_json()
			
		if answer == QMessageBox.StandardButton.No:
			pass
