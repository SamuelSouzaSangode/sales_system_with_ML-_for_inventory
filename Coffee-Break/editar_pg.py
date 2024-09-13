import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, QPushButton,
QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from adicionar_categoria_pg import Adicionar_categoria
from aprender_pg import Aprender

class Editar(QDialog):
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
		
		self.botao_editar = QPushButton('Editar')
		self.botao_editar.setEnabled(False)
		self.botao_editar.clicked.connect(self.editar)
		
		botao_sair = QPushButton('Sair')
		botao_sair.clicked.connect(self.sair)
		

		botoes_h = QHBoxLayout()
		botoes_h.addWidget(self.botao_editar)
		botoes_h.addWidget(botao_sair)

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
		
		self.codigo_tedit.append(self.memoria[titulo]['codigo'])	
		self.botao_editar.setEnabled(True)
		
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
			self.atualizar_pagina()
			self.salvar_json()
			
		if resposta == QMessageBox.StandardButton.No:
			pass
		
	def sair(self):
		self.close()	
		
	def editar(self):
		resposta = QMessageBox.warning(self, 'Editar',
		'Têm certeza que deseja editar esse item?',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.Yes)
		
		if resposta == QMessageBox.StandardButton.Yes:
		
			info = {}
		
			titulo = self.titulos_combo.currentText()
			codigo = self.codigo_tedit.toPlainText()
			categoria = self.categoria_combo.currentText()
		
			info['categoria'] = categoria
			info['codigo'] = codigo
			
			self.memoria[titulo] = info
		
			self.barra_pesquisa_itens.clear()

			
			self.salvar_json()
			self.botao_editar.setEnabled(False)
		else:
			pass
		
	def adicionar_categoria(self):
		self.window = Adicionar_categoria()
		self.window.show()
		
	def aprender(self):
		self.window = Aprender()
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
	window = Editar()
	sys.exit(app.exec())

