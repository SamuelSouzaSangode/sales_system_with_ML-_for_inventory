import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit,
QPushButton, QLabel, QFormLayout, QDialog)
from PyQt6.QtCore import Qt

class Adicionar_fornecedor(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setFixedSize(600, 200)
		self.fornecedor = {}
		self.carregar_fornecedor()
		self.setWindowTitle('Adicionar fornecedor')
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
		
		self.fornecedor_ed = QLineEdit()
		self.fornecedor_ed.setClearButtonEnabled(True)
		self.fornecedor_ed.setStyleSheet(estilo_ed)
		
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
		main_form.addRow('Fornecedor', self.fornecedor_ed)
		main_form.addRow('Telefone 1', self.telefone_1_ed)
		main_form.addRow('Telefone 2', self.telefone_2_ed)
		main_form.addRow('E-Mail', self.email_ed)
		main_form.addRow('Endereço', self.endereco_ed)
		main_form.addRow('Fornecimento de?', self.fornecimento_ed)
		main_form.addRow(self.adicionar_botao)
		self.setLayout(main_form)

	def adicionar(self):
		fornecedor = self.fornecedor_ed.text()
		
		info = {}
		
		info['telefone_1'] = self.telefone_1_ed.text()
		info['telefone_2'] = self.telefone_2_ed.text()
		info['email'] = self.email_ed.text()
		info['endereco'] = self.endereco_ed.text()
		info['forn'] = self.fornecimento_ed.text()
		self.fornecedor [fornecedor] = info
		
		self.fornecedor_ed.clear()
		self.telefone_1_ed.clear()
		self.telefone_2_ed.clear()
		self.email_ed.clear()
		self.endereco_ed.clear()
		self.fornecimento_ed.clear()
		
		self.salvar_fornecedor_json()
		self.carregar_fornecedor()
		
		
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
