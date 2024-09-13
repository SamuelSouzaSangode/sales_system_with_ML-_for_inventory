import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit, 
QComboBox, QPushButton, QVBoxLayout, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Adicionar_categoria(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(550, 100)
		self.move(820, 80)
		self.setWindowTitle('Adicinar - Excluir Categoria')
		self.categorias = []
		self.carregar_lista_categorias_json()
		self.setUpMainWindow()
		self.show()
	
	def setUpMainWindow(self):
		self.nova_categoria_ed = QLineEdit()
		self.nova_categoria_ed.setPlaceholderText('Nova categoria...')
		
		botao_nova_categoria = QPushButton('Adicionar Categoria')
		botao_nova_categoria.clicked.connect(self.nova_categoria_salvar)
		
		self.categoria_combo = QComboBox()
		
		botao_excluir_categoria = QPushButton('Excluir Categoria')
		botao_excluir_categoria.clicked.connect(self.excluir_categoria_salvar)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.nova_categoria_ed)
		main_v_box.addWidget(botao_nova_categoria)
		main_v_box.addWidget(self.categoria_combo)
		main_v_box.addWidget(botao_excluir_categoria)
		self.setLayout(main_v_box)
		self.atualizar_pagina()
	
	def nova_categoria_salvar(self):
		entrada = self.nova_categoria_ed.text()
		if entrada != '':
			self.categorias.append(entrada)
			self.salvar_lista_categorias_json()
			self.atualizar_pagina()
			print(self.categorias)
			
	def excluir_categoria_salvar(self):
		categoria = self.categoria_combo.currentText()
		self.categorias.remove(categoria)
		self.salvar_lista_categorias_json()
		self.atualizar_pagina()
		
	def atualizar_pagina(self):
		self.carregar_lista_categorias_json()
		self.nova_categoria_ed.clear()
		self.categoria_combo.clear()
		self.categoria_combo.addItems(self.categorias)
	
		
		
		
		
	def salvar_lista_categorias_json(self):
		try:
			with open('categorias.json', 'w') as file:
				json.dump(self.categorias, file)
		except FileNotFoundError:
			print('O arquivo de lista de categorias não encontrado')
	
	def carregar_lista_categorias_json(self):
		try:
			with open('categorias.json', 'r') as file:
				content = file.read()
				if content:
					self.categorias = json.loads(content)
		except (FileNotFoundError, json.JSONDecodeError):
			pass
			
			
		
		
		


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Adicionar_categoria()
	sys.exit(app.exec())
