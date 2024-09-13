import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit,
QPushButton, QVBoxLayout)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Inserir(QWidget):
	def __init__(self):
		super().__init__()
		self.initializeUI()

	
	def initializeUI(self):
		self.resize(400, 300)
		self.setWindowTitle('Adicionar demanda')
		self.demanda = {}
		self.carregar_demanda()
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		self.item = QLineEdit()
		self.demanda_item = QLineEdit()
		confirmar = QPushButton('CONFIRMAR')
		confirmar.clicked.connect(self.confirmar)
		
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(self.item)
		main_v_box.addWidget(self.demanda_item)
		main_v_box.addWidget(confirmar)
		self.setLayout(main_v_box)
		
	def confirmar(self):
		
		item = self.item.text()
		demanda_anual = float(self.demanda_item.text())
		
		self.demanda[item] = demanda_anual
		print(self.demanda)
		
		self.item.clear()
		self.demanda_item.clear()
		self.salvar_demanda()
		
	def carregar_demanda(self):
		try:
			with open('base_data/demanda.json', 'r') as file:
				content = file.read()
				if content:
					self.demanda.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Demanda não encontrada')	
			
	def salvar_demanda(self):
		try:
			with open('base_data/demanda.json', 'w') as file:
				json.dump(self.demanda, file)
		
		except FileNotFoundError:
			print('errorrrrr')
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Inserir()
	sys.exit(app.exec())
