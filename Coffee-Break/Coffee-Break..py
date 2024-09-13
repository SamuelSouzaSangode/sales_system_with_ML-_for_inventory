import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, QPushButton,
QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from adicionar_categoria_pg import Adicionar_categoria
from aprender_pg import Aprender
from editar_pg import Editar

class MainWindow(QWidget):
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
		self.categoria_combo.currentTextChanged.connect(self.combo_box_titulos)
		
		self.titulos_combo = QComboBox()

		
		self.barra_pesquisa_itens = QLineEdit()
		self.barra_pesquisa_itens.setClearButtonEnabled(True)
		self.barra_pesquisa_itens.textEdited.connect(self.combo_box_titulos)
		
		self.codigo_tedit = QTextEdit()
		
		botao_pesquisar = QPushButton('Pesquisar')
		botao_pesquisar.clicked.connect(self.pesquisar)
		
		botao_adicionar_categoria = QPushButton('Ad Categoria')
		botao_adicionar_categoria.clicked.connect(self.adicionar_categoria)
		

		botao_aprender = QPushButton('Aprender')
		botao_aprender.clicked.connect(self.aprender)

		botao_editar = QPushButton('Editar')
		botao_editar.clicked.connect(self.editar)
		
		botao_deletar = QPushButton('Deletar')
		botao_deletar.clicked.connect(self.deletar)
		
		botao_atualizar = QPushButton('Atualizar')
		botao_atualizar.clicked.connect(self.atualizar_pagina)

		botoes_h = QHBoxLayout()
		botoes_h.addWidget(botao_adicionar_categoria)
		botoes_h.addWidget(botao_aprender)
		botoes_h.addWidget(botao_editar)
		botoes_h.addWidget(botao_deletar)
		botoes_h.addWidget(botao_atualizar)


		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.categoria_combo)
		main_v_box.addWidget(self.barra_pesquisa_itens)
		main_v_box.addWidget(self.titulos_combo)
		main_v_box.addWidget(botao_pesquisar)
		main_v_box.addWidget(self.codigo_tedit)
		main_v_box.addLayout(botoes_h)
		self.setLayout(main_v_box)
		
		self.atualizar_pagina()
		self.combo_box_titulos()

	
	def atualizar_pagina(self):
		self.carregar_lista_categorias_json()
		self.carregar_dic_memoria_json()
		
		self.categoria_combo.clear()
		self.barra_pesquisa_itens.clear()	
		self.codigo_tedit.clear()	
		
		self.categoria_combo.addItems(self.categorias)
		

	def combo_box_titulos(self):
		self.codigo_tedit.clear()
		self.titulos_combo.clear()
		self.lista_titulos = []
		categoria = self.categoria_combo.currentText()
		
		if self.barra_pesquisa_itens.text() == '':
			for titulo, info in self.memoria.items():
				if categoria == info['categoria']:
				
					self.lista_titulos.append(titulo)
					
		if self.barra_pesquisa_itens.text() != '':
			for titulo, info in self.memoria.items():
				if categoria == info['categoria']:
					if self.barra_pesquisa_itens.text() in titulo:
						self.lista_titulos.append(titulo)
					
		self.titulos_combo.addItems(self.lista_titulos)

		
	def pesquisar(self):
		self.codigo_tedit.clear()
		titulo = self.titulos_combo.currentText()
		try:
			self.codigo_tedit.append(self.memoria[titulo]['codigo'])
		except:
			pass	
		
	def deletar(self):
		titulo = self.titulos_combo.currentText()
		
		resposta = QMessageBox.warning(self, 'Deletar Título',
		f'''<p>Tem certeza que deseja deletar o Título: {titulo}</p>
		<p> depois de deletado não será mais possível recuperá-lo</p>''',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.No)
		
		if resposta == QMessageBox.StandardButton.Yes:
			del self.memoria[titulo]
			self.salvar_json()
			self.atualizar_pagina()
			
			
		if resposta == QMessageBox.StandardButton.No:
			pass
		
		
		


				
			
		
	
	def adicionar_categoria(self):
		self.window = Adicionar_categoria()
		self.window.show()
		
	def aprender(self):
		self.window = Aprender()
		self.window.show()
	
	def editar(self):
		self.window = Editar()
		self.window.show()
		
	def carregar_dic_memoria_json(self):
		try:
			with open('memoria.json', 'r') as file:
				content = file.read()
				if content:
					self.memoria.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			pass
			
	def carregar_lista_categorias_json(self):
		try:
			with open('categorias.json', 'r') as file:
				content = file.read()
				if content:
					self.categorias = json.loads(content)
		except (FileNotFoundError, json.JSONDecodeError):
			pass	
		
	def salvar_json(self):
		try:
			with open('memoria.json', 'w') as file:
				json.dump(self.memoria, file)
				
		except FileNotFoundError:
			pass
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())
