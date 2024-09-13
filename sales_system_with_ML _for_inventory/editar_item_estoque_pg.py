import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, 
QPushButton, QMessageBox, QDialog, QComboBox, QTextEdit,
QFormLayout, QLabel)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Editar_item_dialog(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(400, 100)
		self.setWindowTitle('Editar item no estoque')
		self.estoque = {}
		self.categoria = []
		self.subcategoria = []
		self.fornecedor = {}
		self.carregar_categoria()
		self.carregar_sub_categoria()
		self.carregar_estoque_json()
		self.carregar_fornecedor()
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		
		#Estilo de todos os edits
		self.ed_style = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		#Estilo de todos os botões
		estilo_botao = '''
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		'''
		
		self.pesquisa_ed = QLineEdit()
		self.pesquisa_ed.setStyleSheet(self.ed_style)
		self.pesquisa_ed.setClearButtonEnabled(True)
		self.pesquisa_ed.setPlaceholderText('Pesquisar item...')
		self.pesquisa_ed.textEdited.connect(self.pesquisa_combo)
		
		
		self.item_combo = QComboBox()
		self.item_combo.setStyleSheet(self.ed_style)
		self.pesquisa_combo()
		
		self.item_combo.currentIndexChanged.connect(self.set_info)
		
		
		

		
		
		self.codigo_ed = QLineEdit()
		self.codigo_ed.setMaximumWidth(200)
		self.codigo_ed.setClearButtonEnabled(True)
		self.codigo_ed.setStyleSheet(self.ed_style)
		
		self.item_ed = QLabel()
		self.item_ed.setMaximumWidth(500)
		
	
		
		self.categoria_cb = QComboBox()
		self.categoria_cb.addItems(self.categoria)
		self.categoria_cb.setMaximumWidth(200)
		self.categoria_cb.setStyleSheet(self.ed_style)
		
		self.subcategoria_cb = QComboBox()
		self.subcategoria_cb.addItems(self.subcategoria)
		self.subcategoria_cb.setMaximumWidth(200)
		self.subcategoria_cb.setStyleSheet(self.ed_style)
		
		self.fornecedor_cb = QComboBox()
		self.fornecedor_cb.setMaximumWidth(200)
		self.fornecedor_cb.setStyleSheet(self.ed_style)
		self.fornecedor_cb.addItems(list(self.fornecedor.keys()))
		
		self.marca_ed = QLineEdit()
		self.marca_ed.setMaximumWidth(200)
		self.marca_ed.setClearButtonEnabled(True)
		self.marca_ed.setStyleSheet(self.ed_style)
		
		
		self.localizacao_ed = QLineEdit()
		self.localizacao_ed.setMaximumWidth(200)
		self.localizacao_ed.setClearButtonEnabled(True)
		self.localizacao_ed.setStyleSheet(self.ed_style)
		
		self.preco_ed = QLineEdit()
		self.preco_ed.setMaximumWidth(200)
		self.preco_ed.setClearButtonEnabled(True)
		self.preco_ed.setPlaceholderText('Não use " , "')
		self.preco_ed.setStyleSheet(self.ed_style)
		self.preco_ed.textEdited.connect(self.apenas_num_pont_preco)
	
		
		self.custo_ed = QLineEdit()
		self.custo_ed.setMaximumWidth(200)
		self.custo_ed.setClearButtonEnabled(True)
		self.custo_ed.setPlaceholderText('Não use " , "')
		self.custo_ed.setStyleSheet(self.ed_style)
		self.custo_ed.textEdited.connect(self.apenas_num_pont_custo)
		
		
		self.quantidade_ed = QLineEdit()
		self.quantidade_ed.setMaximumWidth(200)
		self.quantidade_ed.setClearButtonEnabled(True)
		self.quantidade_ed.setPlaceholderText('Não use "  ,  "')
		self.quantidade_ed.setStyleSheet(self.ed_style)
		self.quantidade_ed.textEdited.connect(self.apenas_num_pont_quantidade)
		
		
		self.confirmar_botao = QPushButton('Confirmar')
		self.confirmar_botao.setStyleSheet(estilo_botao)
		self.confirmar_botao.clicked.connect(self.salvar_item_estoque)
		
		
		main_form = QFormLayout()
		main_form.setFieldGrowthPolicy(
		main_form.FieldGrowthPolicy.AllNonFixedFieldsGrow)
		main_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft |\
									Qt.AlignmentFlag.AlignTop)
		main_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
		
		main_form.addRow(self.pesquisa_ed)
		main_form.addRow(self.item_combo)
		main_form.addRow('Código*', self.codigo_ed)
		main_form.addRow('Item*', self.item_ed)
		main_form.addRow('Categoria', self.categoria_cb)
		main_form.addRow('SubCategoria', self.subcategoria_cb)
		main_form.addRow('Marca', self.marca_ed)
		main_form.addRow('Fornecedor', self.fornecedor_cb)
		main_form.addRow('Localização', self.localizacao_ed)
		main_form.addRow('Preço de venda*', self.preco_ed)
		main_form.addRow('Custo*', self.custo_ed)
		main_form.addRow('Quantidade*', self.quantidade_ed)
		main_form.addRow(self.confirmar_botao)
		
		
		self.setLayout(main_form)
		self.set_info()
		
	def carregar_estoque_json(self):
		
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu estoque')
			
	def salvar_json(self):
		try:
			with open('base_data/estoque.json', 'w') as file:
				json.dump(self.estoque, file)
		except (FileNotFoundError):
			print('Problema com pasta estoque.json')
		
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
	
	def carregar_fornecedor(self):
		try:
			with open('base_data/fornecedor.json', 'r') as file:
				content = file.read()
				if content:
					self.fornecedor.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu fornecedor')	
	
	def salvar_item_estoque(self):
		ie = self.item_combo.currentText()
		
		if (self.item_ed.text() != '' 
			and self.preco_ed.text() != ''
			and self.custo_ed.text() != ''
			and self.codigo_ed.text() != ''
			and self.quantidade_ed.text() != ''):
				try:
						
					self.info = {}
			
					self.info['codigo'] = self.codigo_ed.text()
					self.info['valor'] = float(self.preco_ed.text())
					self.info['custo'] = float(self.custo_ed.text())
					self.info['quantidade'] = float(self.quantidade_ed.text())
					self.info['fornecedor'] = self.fornecedor_cb.currentText()
					self.info['categoria'] = self.categoria_cb.currentText()
					self.info['subcategoria'] = self.subcategoria_cb.currentText()
					self.info['marca'] = self.marca_ed.text()
					self.info['localizacao'] = self.localizacao_ed.text()
			
					self.estoque[ie] = self.info
			
					self.salvar_json()
			
					self.codigo_ed.clear()
					self.item_ed.clear()
					self.marca_ed.clear()
					self.localizacao_ed.clear()
					self.preco_ed.clear()
					self.custo_ed.clear()
					self.quantidade_ed.clear()
				except ValueError:
					QMessageBox.warning(self, 'Formato não suportado',
					'Verifique o formato "Preço, Custo, Quantidade"',
					QMessageBox.StandardButton.Ok,
					QMessageBox.StandardButton.Ok)
		else:
			QMessageBox.warning(self, 'Error',
			'''<p> Verifique se você preencheu
				todos os campos OBRIGATÓRIOS ' * '</p>''',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
	#Aceita apenas números e '.' para evitar error de calculos	
	
	def apenas_num_pont_preco(self):
		
		for char in self.preco_ed.text():
			if not char.isdigit() and char != '.':
				self.preco_ed.clear()
			else:
				a=0
	
	#Aceita apenas números e '.' para evitar error de calculos		
	def apenas_num_pont_custo(self):
		for char in self.custo_ed.text():
			if not char.isdigit() and char != '.':
				self.custo_ed.clear()
			else:
				a=0
				
	def apenas_num_pont_quantidade(self):
		for char in self.quantidade_ed.text():
			if not char.isdigit() and char != '.':
				self.quantidade_ed.clear()
			else:
				a=0
		
	def pesquisa_combo(self):
		itens = []
		self.item_combo.clear()
		item = self.item_combo.currentText()
		
		
		if self.pesquisa_ed.text() == '':
			self.item_combo.addItems(list(self.estoque.keys()))
			
		else:
			for item, info in self.estoque.items():
				if self.pesquisa_ed.text() in item:
					itens.append(item)
		
			self.item_combo.addItems(itens)
			
	def set_info(self):

		item = self.item_combo.currentText()
		
		if item != '':
			self.codigo_ed.setText(str(self.estoque[item]['codigo']))
			self.item_ed.setText(str(item))
			self.categoria_cb.setCurrentText(str(self.estoque[item]['categoria']))
			self.subcategoria_cb.setCurrentText(str(self.estoque[item]['subcategoria']))
			self.marca_ed.setText(str(self.estoque[item]['marca']))
			self.fornecedor_cb.setCurrentText(str(self.estoque[item]['fornecedor']))
			#self.localizacao_ed.setText(str(self.estoque[item]['localizacao']))
			self.preco_ed.setText(str(self.estoque[item]['valor']))
			self.custo_ed.setText(str(self.estoque[item]['custo']))
			self.quantidade_ed.setText(str(self.estoque[item]['quantidade']))
			
		else:
			pass
		
	
		
		
