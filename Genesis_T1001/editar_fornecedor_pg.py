import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit,
QPushButton, QLabel, QFormLayout, QDialog, QComboBox)
from PyQt6.QtCore import Qt

class Editar_fornecedor(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(600, 200)
		self.fornecedor = {}
		self.carregar_fornecedor()
		self.setWindowTitle('Editar fornecedor')
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		#Estilo de todos os edits
		estilo_ed = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		#Estilo de todos os botões
		estilo_botao = '''
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 5px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		'''
		
		self.pesquisa_forn = QLineEdit()
		self.pesquisa_forn.setClearButtonEnabled(True)
		self.pesquisa_forn.setPlaceholderText('Pesquisar Fornecedor...')
		self.pesquisa_forn.setStyleSheet(estilo_ed)
		self.pesquisa_forn.textEdited.connect(self.forns_combo)
		
		self.forn_combo = QComboBox()
		self.forn_combo.setStyleSheet(estilo_ed)
		self.forns_combo()
		self.forn_combo.currentIndexChanged.connect(self.set_info)
		
		self.fornecedor_label = QLabel()
		self.fornecedor_label.setStyleSheet(estilo_ed)
		
		self.telefone_1_ed = QLineEdit()
		self.telefone_1_ed.setClearButtonEnabled(True)
		self.telefone_1_ed.setStyleSheet(estilo_ed)
		
		self.telefone_2_ed = QLineEdit()
		self.telefone_2_ed.setClearButtonEnabled(True)
		self.telefone_2_ed.setStyleSheet(estilo_ed)
		
		self.email_ed = QLineEdit()
		self.email_ed.setClearButtonEnabled(True)
		self.email_ed.setStyleSheet(estilo_ed)
		
		self.endereco_ed = QLineEdit()
		self.endereco_ed.setClearButtonEnabled(True)
		self.endereco_ed.setStyleSheet(estilo_ed)
		
		self.fornecimento_ed = QLineEdit()
		self.fornecimento_ed.setClearButtonEnabled(True)
		self.fornecimento_ed.setStyleSheet(estilo_ed)
		
		self.adicionar_botao = QPushButton('Confirmar')
		self.adicionar_botao.setStyleSheet(estilo_botao)
		self.adicionar_botao.clicked.connect(self.adicionar)
		
		main_form = QFormLayout()
		main_form = QFormLayout()
		main_form.setFieldGrowthPolicy(
		main_form.FieldGrowthPolicy.AllNonFixedFieldsGrow)
		main_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft |\
									Qt.AlignmentFlag.AlignTop)
		main_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
		main_form.addRow(self.pesquisa_forn)
		main_form.addRow(self.forn_combo)
		main_form.addRow('Fornecedor', self.fornecedor_label)
		main_form.addRow('Telefone 1', self.telefone_1_ed)
		main_form.addRow('Telefone 2', self.telefone_2_ed)
		main_form.addRow('E-Mail', self.email_ed)
		main_form.addRow('Endereço', self.endereco_ed)
		main_form.addRow('Fornecimento de?', self.fornecimento_ed)
		main_form.addRow(self.adicionar_botao)
		self.setLayout(main_form)
		self.set_info()
	
	def adicionar(self):
		fornecedor = self.forn_combo.currentText()
		
		info = {}
		
		info['telefone_1'] = self.telefone_1_ed.text()
		info['telefone_2'] = self.telefone_2_ed.text()
		info['email'] = self.email_ed.text()
		info['endereco'] = self.endereco_ed.text()
		info['forn'] = self.fornecimento_ed.text()
		self.fornecedor [fornecedor] = info
		
		
		self.telefone_1_ed.clear()
		self.telefone_2_ed.clear()
		self.email_ed.clear()
		self.endereco_ed.clear()
		self.fornecimento_ed.clear()
		
		self.salvar_fornecedor_json()
		self.carregar_fornecedor()
		
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
	
	def set_info(self):
		forn = self.forn_combo.currentText()
		
		if forn != '':
			self.fornecedor_label.setText(forn)
			self.telefone_1_ed.setText(self.fornecedor[forn]['telefone_1'])
			self.telefone_2_ed.setText(self.fornecedor[forn]['telefone_2'])
			self.email_ed.setText(self.fornecedor[forn]['email'])
			self.endereco_ed.setText(self.fornecedor[forn]['endereco'])
			self.fornecimento_ed.setText(self.fornecedor[forn]['forn'])
			
		else:
			pass	
		
	def salvar_fornecedor_json(self):
		try:
			with open('base_data/fornecedor.json', 'w') as file:
				json.dump(self.fornecedor, file)
		except (FileNotFoundError):
			print('Problema com pasta fornecedor.json')
		
		
	def carregar_fornecedor(self):
		try:
			with open('base_data/fornecedor.json', 'r') as file:
				content = file.read()
				if content:
					self.fornecedor.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu fornecedor')




