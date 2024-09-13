import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton,
QComboBox, QLineEdit, QDialog, QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt


class Ajustar_custo_preco(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.setMaximumHeight(200)
		self.setMaximumWidth(200)
		self.setWindowTitle('Ajuste de Preço e Custo indexado')
		self.categoria = []
		self.subcategoria = []
		self.estoque = {}
		self.carregar_estoque()
		self.carregar_categoria()
		self.carregar_sub_categoria()
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		self.ed_style = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		estilo_botao = """
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 5px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""
	
		self.total_bt = QPushButton('Todos')
		self.total_bt.clicked.connect(self.todos)
		self.total_bt.setStyleSheet(estilo_botao)
		
		self.categoria_bt = QPushButton('Categoria')
		self.categoria_bt.clicked.connect(self.categoria_ajuste)
		self.categoria_bt.setStyleSheet(estilo_botao)
		
		self.subcategoria_bt = QPushButton('SubCategoria')
		self.subcategoria_bt.clicked.connect(self.subcategoria_ajuste)
		self.subcategoria_bt.setStyleSheet(estilo_botao)
		
		self.fornecedor_bt = QPushButton('Fornecedor')
		self.fornecedor_bt.setEnabled(False)
		self.fornecedor_bt.setStyleSheet(estilo_botao)
		
		self.marca_bt = QPushButton('Marca')
		self.marca_bt.setEnabled(False)
		self.marca_bt.setStyleSheet(estilo_botao)
		
		self.escolha_combo = QComboBox()
		self.escolha_combo.setStyleSheet(self.ed_style)
		
		self.porcentagem_valor_ed = QLineEdit()
		self.porcentagem_valor_ed.setPlaceholderText("Não use ' % '...")
		self.porcentagem_valor_ed.textEdited.connect(self.apenas_num_pont_porcentagem_valor)
		self.porcentagem_valor_ed.setStyleSheet(self.ed_style)
		
		self.porcentagem_custo_ed = QLineEdit()
		self.porcentagem_custo_ed.setPlaceholderText("Não use ' % '...")
		self.porcentagem_custo_ed.textEdited.connect(self.apenas_num_pont_porcentagem_custo)
		self.porcentagem_custo_ed.setStyleSheet(self.ed_style)
		
		self.confirmar_bt = QPushButton('Confirmar')
		self.confirmar_bt.clicked.connect(self.confirmar_botao)
		self.confirmar_bt.setStyleSheet(estilo_botao)
		
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.total_bt)
		main_v_box.addWidget(self.categoria_bt)
		main_v_box.addWidget(self.subcategoria_bt)
		main_v_box.addWidget(self.fornecedor_bt)
		main_v_box.addWidget(self.marca_bt)
		main_v_box.addWidget(self.escolha_combo)
		main_v_box.addWidget(self.porcentagem_valor_ed)
		main_v_box.addWidget(self.porcentagem_custo_ed)
		main_v_box.addWidget(self.confirmar_bt)
		self.setLayout(main_v_box)
		
		
	def todos(self):
		self.escolha_combo.clear()
		todos = ['Todos']
		self.escolha_combo.addItems(todos)
		
	def categoria_ajuste(self):
		self.escolha_combo.clear()
		self.escolha_combo.addItems(self.categoria)
		
	def subcategoria_ajuste(self):
		self.escolha_combo.clear()
		self.escolha_combo.addItems(self.subcategoria)
		
	def confirmar_botao(self):
		porc_preco = self.porcentagem_valor_ed.text()
		porc_custo = self.porcentagem_custo_ed.text()
		escolha = self.escolha_combo.currentText()
		
		answer = QMessageBox.warning(self, 'Ajuste Preço e Custo',
		f'''<p> Todos itens selecionados em  serão ajustados</p>
		<p> Preço em {porc_preco} %</p>
		<p> Custo em {porc_custo} %</p>''',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.No)
		
		if answer == QMessageBox.StandardButton.Yes:
			
			if escolha == 'Todos':
				for item, info in self.estoque.items():
					custo = (((self.estoque[item]['custo']*(float(porc_custo) /100))) + (self.estoque[item]['custo']))
					valor= (((self.estoque[item]['valor']*(float(porc_preco) /100))) + (self.estoque[item]['valor']))
					custo_form = round(custo, 2)
					valor_form = round(valor, 2)
					self.estoque[item]['custo'] = custo_form
					self.estoque[item]['valor'] = valor_form
			else:
				
				for item, info in self.estoque.items():
					for info_item, valor in info.items():
						if valor == escolha:
							custo = (((self.estoque[item]['custo']*(float(porc_custo) /100))) + (self.estoque[item]['custo']))
							valor = (((self.estoque[item]['valor']*(float(porc_preco) /100))) + (self.estoque[item]['valor']))
							custo_form = round(custo, 2)
							valor_form = round(valor, 2)
							self.estoque[item]['custo'] = custo_form
							self.estoque[item]['valor'] = valor_form
						
							
						else:
							pass

		self.salvar_estoque_json()				
						
	def apenas_num_pont_porcentagem_valor(self):
		for char in self.porcentagem_valor_ed.text():
			if not char.isdigit() and char != '.':
				self.porcentagem_valor_ed.clear()
			else:
				a=0					
	
	def apenas_num_pont_porcentagem_custo(self):
		for char in self.porcentagem_custo_ed.text():
			if not char.isdigit() and char != '.':
				self.porcentagem_custo_ed.clear()
			else:
				a=0
		
	def carregar_categoria(self):
		try:
			with open('base_data/categoria.json', 'r') as file:
				content = file.read()
				if content:
					self.categoria = (json.loads(content))
					
		except (FileNotFoundError, json.JSONDecodeError):
			pass
	
	def carregar_sub_categoria(self):
		try:
			with open('base_data/subcategoria.json', 'r') as file:
				content = file.read()
				if content:
					self.subcategoria = (json.loads(content))
					
		except (FileNotFoundError, json.JSONDecodeError):
			pass 
	
	def carregar_estoque(self):
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu estoque')
	
	def salvar_estoque_json(self):
		try:
			with open('base_data/estoque.json', 'w') as file:
				json.dump(self.estoque, file)
		except (FileNotFoundError):
			print('Problema com pasta estoque.json')
	

