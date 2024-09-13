import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton,
QLabel, QVBoxLayout, QDialog, QComboBox, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt

class Divida(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		
		self.cliente = {}
		self.carregar_cliente()
		self.setWindowTitle('Editar cliente')
		self.setUpMainWindow()
		self.move(320, 190)
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
		self.cliente_combo = QComboBox()
		self.cliente_combo.setStyleSheet(estilo_ed)
		self.clientes_combo()
		self.cliente_combo.currentIndexChanged.connect(self.set_info)
		
		self.cliente_divida_ed = QLineEdit()
		self.cliente_divida_ed.setStyleSheet(estilo_ed)
		self.cliente_divida_ed.textEdited.connect(self.apenas_num_pont_divida)
		
		self.label = QLabel('R$ ')
		
		main_h_box = QHBoxLayout()
		main_h_box.addWidget(self.label)
		main_h_box.addWidget(self.cliente_divida_ed)
		
		confirmar_botao = QPushButton('Confirmar')
		confirmar_botao.setStyleSheet(estilo_botao)
		confirmar_botao.clicked.connect(self.botao_confirmar)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.cliente_combo)
		main_v_box.addLayout(main_h_box)
		main_v_box.addWidget(confirmar_botao)
		self.setLayout(main_v_box)
		
		self.set_info()

	def apenas_num_pont_divida(self):
		
		for char in self.cliente_divida_ed.text():
			if not char.isdigit() and char != '.':
				self.cliente_divida_ed.clear()
			else:
				a=0
	
	def botao_confirmar(self):
		cliente = self.cliente_combo.currentText()
		try:
			self.cliente[cliente]['divida'] = float(self.cliente_divida_ed.text())
		
			self.salvar_cliente_json()
		
		except ValueError:
			QMessageBox.warning(self, 'Formato não suportado',
			'Verifique error de digitação na entrada do valor devido!!!',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
	
	def set_info(self):
		cliente = self.cliente_combo.currentText()
		
		if cliente != '':
			self.cliente_divida_ed.setText(str(self.cliente[cliente]['divida']))
			
		else:
			pass	
		
	def clientes_combo(self):
		clientes = []
		self.cliente_combo.clear()
		
		if '' == '':
			self.cliente_combo.addItems(list(self.cliente.keys()))
				
		
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



