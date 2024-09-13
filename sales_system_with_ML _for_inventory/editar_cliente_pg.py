import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit,
QPushButton, QLabel, QFormLayout, QDialog, QComboBox)
from PyQt6.QtCore import Qt

class Editar_cliente(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(600, 200)
		self.cliente = {}
		self.carregar_cliente()
		self.setWindowTitle('Editar cliente')
		self.setUpMainWindow()
		self.move(525, 75)
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
		
		self.pesquisa_cliente = QLineEdit()
		self.pesquisa_cliente.setClearButtonEnabled(True)
		self.pesquisa_cliente.setPlaceholderText('Pesquisar cliente...')
		self.pesquisa_cliente.setStyleSheet(estilo_ed)
		self.pesquisa_cliente.textEdited.connect(self.clientes_combo)
		
		self.cliente_combo = QComboBox()
		self.cliente_combo.setStyleSheet(estilo_ed)
		self.clientes_combo()
		self.cliente_combo.currentIndexChanged.connect(self.set_info)
		
		self.cliente_label = QLabel()
		self.cliente_label.setStyleSheet(estilo_ed)
		
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
		
		self.ramo_de_atividade_ed = QLineEdit()
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
		
		main_form.addRow(self.pesquisa_cliente)
		main_form.addRow(self.cliente_combo)
		main_form.addRow('Fornecedor', self.cliente_label)
		main_form.addRow('Telefone 1', self.telefone_1_ed)
		main_form.addRow('Telefone 2', self.telefone_2_ed)
		main_form.addRow('E-Mail', self.email_ed)
		main_form.addRow('Endereço', self.endereco_ed)
		main_form.addRow('Ramo de ?', self.ramo_de_atividade_ed)
		main_form.addRow(self.adicionar_botao)
		self.setLayout(main_form)
		self.set_info()
	
	def adicionar(self):
		cliente = self.cliente_combo.currentText()
		
		info = {}
		
		info['telefone_1'] = self.telefone_1_ed.text()
		info['telefone_2'] = self.telefone_2_ed.text()
		info['email'] = self.email_ed.text()
		info['endereco'] = self.endereco_ed.text()
		info['atividade'] = self.ramo_de_atividade_ed.text()
		info['divida'] = self.cliente[cliente]['divida']
		self.cliente [cliente] = info
		
		
		self.telefone_1_ed.clear()
		self.telefone_2_ed.clear()
		self.email_ed.clear()
		self.endereco_ed.clear()
		self.ramo_de_atividade_ed.clear()
		
		self.salvar_cliente_json()
		self.carregar_cliente()
		
	def clientes_combo(self):
		clientes = []
		self.cliente_combo.clear()
		
		if self.pesquisa_cliente == '':
			self.cliente_combo.addItems(list(self.cliente.keys()))
		else:
			
			for client, info in self.cliente.items():
				if self.pesquisa_cliente.text() in client:
					clientes.append(client)
					
			self.cliente_combo.addItems(clientes)		
	
	def set_info(self):
		cliente = self.cliente_combo.currentText()
		
		if cliente != '':
			self.cliente_label.setText(cliente)
			self.telefone_1_ed.setText(self.cliente[cliente]['telefone_1'])
			self.telefone_2_ed.setText(self.cliente[cliente]['telefone_2'])
			self.email_ed.setText(self.cliente[cliente]['email'])
			self.endereco_ed.setText(self.cliente[cliente]['endereco'])
			self.ramo_de_atividade_ed.setText(self.cliente[cliente]['atividade'])
			
		else:
			pass	
		
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



if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Editar_cliente()
	sys.exit(app.exec())
