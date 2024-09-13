import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit,
QPushButton, QLabel, QFormLayout, QDialog, QMessageBox)
from PyQt6.QtCore import Qt

class Adicionar_cliente(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setFixedSize(600, 200)
		self.cliente = {}
		self.carregar_cliente()
		self.setWindowTitle('Adicionar Cliente')
		self.setUpMainWindow()
		self.move(330, 90)
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
		
		self.cliente_ed = QLineEdit()
		self.cliente_ed.setClearButtonEnabled(True)
		self.cliente_ed.setStyleSheet(estilo_ed)
		
		self.telefone_1_ed = QLineEdit('(000) 999999999')
		self.telefone_1_ed.setClearButtonEnabled(True)
		self.telefone_1_ed.setStyleSheet(estilo_ed)
		
		self.telefone_2_ed = QLineEdit('(000) 999999999')
		self.telefone_2_ed.setClearButtonEnabled(True)
		self.telefone_2_ed.setStyleSheet(estilo_ed)
		
		self.email_ed = QLineEdit('cliente@email.com')
		self.email_ed.setClearButtonEnabled(True)
		self.email_ed.setStyleSheet(estilo_ed)
		
		self.endereco_ed = QLineEdit('Avenida Endereço do cliente, Número 1111, Bairro Bairro, Brasil')
		self.endereco_ed.setClearButtonEnabled(True)
		self.endereco_ed.setStyleSheet(estilo_ed)
		
		self.ramo_de_atividade_ed = QLineEdit('Atividade, Atividade, Atividade')
		self.ramo_de_atividade_ed.setClearButtonEnabled(True)
		self.ramo_de_atividade_ed.setStyleSheet(estilo_ed)
		
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
		main_form.addRow('Cliente', self.cliente_ed)
		main_form.addRow('Telefone 1', self.telefone_1_ed)
		main_form.addRow('Telefone 2', self.telefone_2_ed)
		main_form.addRow('E-Mail', self.email_ed)
		main_form.addRow('Endereço', self.endereco_ed)
		main_form.addRow('Ramo de atividade', self.ramo_de_atividade_ed)
		main_form.addRow(self.adicionar_botao)
		self.setLayout(main_form)

	def adicionar(self):
		cliente = self.cliente_ed.text()
		if cliente != '':
		
			info = {}
		
			info['telefone_1'] = self.telefone_1_ed.text()
			info['telefone_2'] = self.telefone_2_ed.text()
			info['email'] = self.email_ed.text()
			info['endereco'] = self.endereco_ed.text()
			info['atividade'] = self.ramo_de_atividade_ed.text()
			info['divida'] = 0
			self.cliente [cliente] = info
		
			self.cliente_ed.clear()
			self.telefone_1_ed.clear()
			self.telefone_1_ed.setText('(000) 999999999')
		
			self.telefone_2_ed.clear()
			self.telefone_2_ed.setText('(000) 999999999')
		
			self.email_ed.clear()
			self.email_ed.setText('cliente@email.com')
		
			self.endereco_ed.clear()
			self.endereco_ed.setText('Avenida Endereço do cliente, Número 1111, Bairro Bairro, Brasil')
		
			self.ramo_de_atividade_ed.clear()
			self.ramo_de_atividade_ed.setText('Atividade, Atividade, Atividade')
		
			self.salvar_cliente_json()
			self.carregar_cliente()
		
		else:
			QMessageBox.warning(self, 'Error ao salvar',
			'''Atenção o campo 'Cliente' não pode estar vazio''',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
	
	def salvar_cliente_json(self):
		try:
			with open('base_data/cliente.json', 'w') as file:
				json.dump(self.cliente, file)
		except (FileNotFoundError):
			print('Problema com pasta cliente.json')
		
		
	def carregar_cliente(self):
		try:
			with open('base_data/cliente.json', 'r') as file:
				content = file.read()
				if content:
					self.cliente.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu cliente')
			

