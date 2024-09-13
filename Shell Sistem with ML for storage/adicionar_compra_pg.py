import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit, QComboBox,
QPushButton, QMessageBox, QGridLayout, QLabel, QDialog)
from PyQt6.QtCore import Qt

class Adicionar_compra(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumWidth(600)
		self.setMinimumHeight(100)
		self.estoque = {}
		self.carregar_estoque_json()
		self.setWindowTitle('Adicionar compra no estoque')
		self.setUpMainWindow()
		self.move(320,220)
		self.show()
		
	def setUpMainWindow(self):
		
		estilo_ed = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		estilo_botao = """
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 5px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""
		

		self.pesquisa_ed = QLineEdit()
		self.pesquisa_ed.setMinimumWidth(350)
		self.pesquisa_ed.setPlaceholderText('Pesquisar Item...')
		self.pesquisa_ed.setClearButtonEnabled(True)
		self.pesquisa_ed.textEdited.connect(self.pesquisa_combo)
		self.pesquisa_ed.setStyleSheet(estilo_ed)
		
		self.item_combo = QComboBox()
		self.pesquisa_combo()
		self.item_combo.currentIndexChanged.connect(self.set_info)
		self.item_combo.setStyleSheet(estilo_ed)

		
		self.preco_label = QLabel('Preço: R$')
		self.preco_ed = QLineEdit()
		self.preco_ed.setMaximumWidth(50)
		self.preco_ed.textEdited.connect(self.apenas_num_pont_preco)
		self.preco_ed.setStyleSheet(estilo_ed)
		
		self.custo_label = QLabel('Custo: R$')
		self.custo_ed = QLineEdit()
		self.custo_ed.setMaximumWidth(50)
		self.custo_ed.textEdited.connect(self.apenas_num_pont_custo)
		self.custo_ed.setStyleSheet(estilo_ed)
		
		self.quantidade_label = QLabel('Quantidade Adquirida: ')
		self.quantidade_ed = QLineEdit()
		self.quantidade_ed.setMaximumWidth(100)
		self.quantidade_ed.textEdited.connect(self.apenas_num_pont_quantidade)
		self.quantidade_ed.setStyleSheet(estilo_ed)
		
		self.adicionar_botao = QPushButton('Adicionar')
		self.adicionar_botao.clicked.connect(self.salvar_item_estoque)
		self.adicionar_botao.setStyleSheet(estilo_botao)
		
		
		main_grid = QGridLayout()
		main_grid.addWidget(self.pesquisa_ed, 0,0)
		main_grid.addWidget(self.item_combo, 1, 0)
		main_grid.addWidget(self.preco_label, 1, 1)
		main_grid.addWidget(self.preco_ed, 1, 2)
		main_grid.addWidget(self.custo_label, 1, 3)
		main_grid.addWidget(self.custo_ed, 1, 4)
		main_grid.addWidget(self.quantidade_label, 1, 5)
		main_grid.addWidget(self.quantidade_ed, 1, 6)
		main_grid.addWidget(self.adicionar_botao, 1, 7)
		self.setLayout(main_grid)
		
		self.set_info()
		
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
			self.preco_ed.setText(str(self.estoque[item]['valor']))
			self.custo_ed.setText(str(self.estoque[item]['custo']))
			
	def apenas_num_pont_custo(self):
		for char in self.custo_ed.text():
			if not char.isdigit() and char != '.':
				self.custo_ed.clear()
			else:
				a=0
				
	def apenas_num_pont_preco(self):
		
		for char in self.preco_ed.text():
			if not char.isdigit() and char != '.':
				self.preco_ed.clear()
			else:
				a=0
				
	def apenas_num_pont_quantidade(self):
		for char in self.quantidade_ed.text():
			if not char.isdigit() and char != '.':
				self.quantidade_ed.clear()
			else:
				a=0
		
	def carregar_estoque_json(self):
		
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu estoque')
			
	def salvar_item_estoque(self):
		ie = self.item_combo.currentText()
		
		if (self.preco_ed.text() != ''
			and self.custo_ed.text() != ''
			and self.quantidade_ed.text() != ''):
				
				try:
						
					
			
					
					self.estoque[ie]['valor'] = float(self.preco_ed.text())
					self.estoque[ie]['custo'] = float(self.custo_ed.text())
					self.estoque[ie]['quantidade'] += float(self.quantidade_ed.text())

			
					
			
					self.salvar_json()
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
		
	def salvar_json(self):
		try:
			with open('base_data/estoque.json', 'w') as file:
				json.dump(self.estoque, file)
		except (FileNotFoundError):
			print('Problema com pasta estoque.json')		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Adicionar_compra()
	sys.exit(app.exec())
