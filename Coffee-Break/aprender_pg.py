import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, QPushButton,
QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Aprender(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(550, 696)
		self.move(820, 0)
		self.setWindowTitle('Coffe Break Cod')
		self.categorias = []
		self.carregar_lista_categorias_json()
		self.memoria = {}
		self.carregar_dic_memoria_json()
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		self.categoria_combo = QComboBox()	
		
		self.novo_titulo_ed = QLineEdit()
		
		self.codigo_tedit = QTextEdit()
		

		

		botao_aprender = QPushButton('Aprender')
		botao_aprender.clicked.connect(self.salvar_dic_memoria_json)
		
		botao_sair = QPushButton('Sair')
		botao_sair.clicked.connect(self.sair)
		



		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.categoria_combo)
		main_v_box.addWidget(self.novo_titulo_ed)
		main_v_box.addWidget(self.codigo_tedit)
		main_v_box.addWidget(botao_aprender)
		main_v_box.addWidget(botao_sair)
		self.setLayout(main_v_box)
		self.categoria_combo.addItems(self.categorias)
	def carregar_lista_categorias_json(self):
		try:
			with open('categorias.json', 'r') as file:
				content = file.read()
				if content:
					self.categorias = json.loads(content)
		except (FileNotFoundError, json.JSONDecodeError):
			pass	
			
	def salvar_dic_memoria_json(self):
		info = {}
		titulo = self.novo_titulo_ed.text()
		categoria = self.categoria_combo.currentText()
		codigo = self.codigo_tedit.toPlainText()
		
		info['codigo'] = codigo
		info['categoria'] = categoria
		
		self.memoria[titulo] = info
		
		self.novo_titulo_ed.clear()
		self.codigo_tedit.clear()
		
		self.salvar_json()
		
	def sair(self):
		self.close()

	def salvar_json(self):
		try:
			with open('memoria.json', 'w') as file:
				json.dump(self.memoria, file)
				
		except FileNotFoundError:
			pass
			
	def carregar_dic_memoria_json(self):
		try:
			with open('memoria.json', 'r') as file:
				content = file.read()
				if content:
					self.memoria.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			pass
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Aprender()
	sys.exit(app.exec())
