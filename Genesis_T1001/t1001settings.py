import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit,
QPushButton, QLabel, QMessageBox, QGridLayout, QDialog)
from PyQt6.QtGui import QFont
from  PyQt6.QtCore import Qt

class T1001_configuracoes(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.resize(300, 200)
		self.setWindowTitle('Configurações T1001')
		self.config = {}
		self.carregar_json()
		self.setUpMainWindow()
		self.carregar()
		self.show()
	
	def setUpMainWindow(self):
		ed_estilo = '''
		border-radius: 10px; border: 2px solid gray'''
		
		estilo_botao = """
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 5px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""		

		
		config_label = QLabel('Configurações')
		config_label.setFont(QFont('Arial', 18))
		
		icms_label = QLabel('Icms Decimal: ')
		icms_label.setFont(QFont('Arial', 12))
		
		self.icms_ed = QLineEdit()
		self.icms_ed.setFixedSize(60, 20)
		self.icms_ed.setStyleSheet(ed_estilo)
		
		consumo_estoque_label = QLabel('Consumo anual estoque     R$:')
		consumo_estoque_label.setFont(QFont('Arial', 12))
		
		self.consumo_estoque_ed = QLineEdit()
		self.consumo_estoque_ed.setFixedSize(60, 20)
		self.consumo_estoque_ed.setStyleSheet(ed_estilo)
		
		estoque_maximo_label = QLabel('Estoque Máximo:                 R$:')
		estoque_maximo_label.setFont(QFont('Arial', 12))
		
		self.estoque_maximo_ed = QLineEdit()
		self.estoque_maximo_ed.setFixedSize(60, 20)
		self.estoque_maximo_ed.setStyleSheet(ed_estilo)
		
		estoque_minimo_label = QLabel('Estoque Mínimo:                  R$:')
		estoque_minimo_label.setFont(QFont('Arial', 12))
		
		self.estoque_minimo_ed = QLineEdit()
		self.estoque_minimo_ed.setFixedSize(60, 20)
		self.estoque_minimo_ed.setStyleSheet(ed_estilo)
		
		ultima_compra_label = QLabel('Data ultima compra(dd/mm/yy):')
		ultima_compra_label.setFont(QFont('Arial', 12))
		
		self.data_ultima_compra_ed = QLineEdit()
		self.data_ultima_compra_ed.setFixedSize(60, 20)
		self.data_ultima_compra_ed.setStyleSheet(ed_estilo)
		
		salvar_botao = QPushButton('Salvar')
		salvar_botao.setStyleSheet(estilo_botao)
		salvar_botao.clicked.connect(self.salvar)
		
		
		main_grid = QGridLayout()
		main_grid.addWidget(config_label, 0, 0)
		main_grid.addWidget(icms_label, 1, 0)
		main_grid.addWidget(self.icms_ed, 1, 1)
		main_grid.addWidget(consumo_estoque_label, 2, 0)
		main_grid.addWidget(self.consumo_estoque_ed, 2, 1)
		main_grid.addWidget(estoque_maximo_label, 3, 0)
		main_grid.addWidget(self.estoque_maximo_ed, 3, 1)
		main_grid.addWidget(estoque_minimo_label, 4, 0)
		main_grid.addWidget(self.estoque_minimo_ed, 4, 1)
		main_grid.addWidget(ultima_compra_label, 5, 0)
		main_grid.addWidget(self.data_ultima_compra_ed, 5, 1)
		main_grid.addWidget(salvar_botao, 6, 0, 1, 2)
		
		
		
		self.setLayout(main_grid)
	
	def salvar(self):
		try:
			icms = float(self.icms_ed.text())
			consumo_estoque_anual = float(self.consumo_estoque_ed.text())
			estoque_maximo = float(self.estoque_maximo_ed.text())
			estoque_minimo = float(self.estoque_minimo_ed.text())
			data_ultima_compra = str(self.data_ultima_compra_ed.text())
			self.config['icms'] = icms
			self.config['estoque_anual'] = consumo_estoque_anual
			self.config['estoque_maximo'] = estoque_maximo
			self.config['estoque_minimo'] = estoque_minimo
			self.config['data_ultima_compra'] = data_ultima_compra
			self.salvar_json()
			self.close()
			
		except ValueError:
			QMessageBox.warning(self, 'Formato não suportado',
			'Confira as informações inseridas, não use caractere nem vírgulas, use pontos.',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
		
	
	def carregar(self):
		
		self.icms_ed.setText(str(self.config['icms']))
		self.consumo_estoque_ed.setText(str(self.config['estoque_anual'] ))
		self.estoque_maximo_ed.setText(str(self.config['estoque_maximo'] ))
		self.estoque_minimo_ed.setText(str(self.config['estoque_minimo'] ))
		self.data_ultima_compra_ed.setText(self.config['data_ultima_compra'] )
	
	def salvar_json(self):
		try:
			with open('base_data/config.json', 'w') as file:
				json.dump(self.config, file)
				
		except FileNotFoundError:
			pass
		
	def carregar_json(self):
		try:
			with open('base_data/config.json', 'r') as file:
				content = file.read()
				if content:
					self.config.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			pass
				
		
