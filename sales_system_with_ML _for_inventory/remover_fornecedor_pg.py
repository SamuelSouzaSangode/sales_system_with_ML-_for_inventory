import json, sys
from PyQt6.QtWidgets import (QWidget, QApplication,QLineEdit,
QPushButton, QComboBox, QVBoxLayout, QMessageBox, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Remover_fornecedor(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.setMinimumWidth(100)
		self.setMinimumHeight(100)
		self.setWindowTitle('Remover item')
		self.fornecedor = {}
		self.carregar_fornecedor()
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
		
		self.pesquisa_forn = QLineEdit()
		self.pesquisa_forn.setPlaceholderText('Del. Items')
		self.pesquisa_forn.textEdited.connect(self.forns_combo)
		self.pesquisa_forn.setStyleSheet(self.ed_style)
		
		self.forn_combo = QComboBox()
		self.forn_combo.setStyleSheet(self.ed_style)
		self.forns_combo()
		
		self.remover_bt = QPushButton('Remover')
		self.remover_bt.setStyleSheet(estilo_botao)
		self.remover_bt.clicked.connect(self.remover)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.pesquisa_forn)
		main_v_box.addWidget(self.forn_combo)
		main_v_box.addWidget(self.remover_bt)
		self.setLayout(main_v_box)
		
	def forns_combo(self):
		forns = []
		self.forn_combo.clear()
		
		if self.pesquisa_forn == '':
			self.forn_combo.addItems(list(self.fornecedor.keys()))
		else:
			
			for forn, info in self.fornecedor.items():
				if self.pesquisa_forn.text() in forn:
					forns.append(forn)
					
			self.forn_combo.addItems(forns)
					
		
	def carregar_fornecedor(self):
		try:
			with open('base_data/fornecedor.json', 'r') as file:
				content = file.read()
				if content:
					self.fornecedor.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu fornecedor')
			
	def salvar_json(self):
		try:
			with open('base_data/fornecedor.json', 'w') as file:
				json.dump(self.fornecedor, file)
		except (FileNotFoundError):
			print('Problema com pasta estoque.json')

	def remover(self):
		forn = self.forn_combo.currentText()
		
		answer = QMessageBox.warning(self, 'Excluir fornecedor',
		f'''<p>Excluir o Fornecedor: {forn} !?</p>''',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.No)
		
		if answer == QMessageBox.StandardButton.Yes:
			if forn != '':
				del self.fornecedor[forn]
				self.forn_combo.clear()
				self.forn_combo.addItems(list(self.fornecedor))
				self.salvar_json()
			if forn == '':
				pass
			
		if answer == QMessageBox.StandardButton.No:
			pass



