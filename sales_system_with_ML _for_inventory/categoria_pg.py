import sys, json
from PyQt6.QtWidgets import (QWidget, QApplication, QLineEdit, 
QComboBox, QPushButton, QLabel, QMessageBox, QVBoxLayout, QDialog)

class Adicionar_Categoria(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
	
	def initializeUI(self):
		self.setMinimumWidth(200)
		self.setMinimumHeight(50)
		self.setWindowTitle('Adicionar Categoria')
		self.categoria = []
		self.carregar_categoria()
		self.setUpMainWindow()
		self.move(320, 260)
		self.show()
		
	def setUpMainWindow(self):
		
		self.ed_style = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		estilo_botao = '''
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 4px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		'''
		
		
		
		self.adicionar_categoria_ed = QLineEdit()
		self.adicionar_categoria_ed.setPlaceholderText('Ad. Categoria')
		self.adicionar_categoria_ed.setStyleSheet(self.ed_style)
		
		self.adicionar_categoria_bt = QPushButton('Adicionar Categoria')
		self.adicionar_categoria_bt.setStyleSheet(estilo_botao)
		self.adicionar_categoria_bt.clicked.connect(self.adicionar_combo)
		
		
		self.categoria_combo = QComboBox()
		self.categoria_combo.setStyleSheet(self.ed_style)
		self.categoria_combo.addItems(self.categoria)
		
		self.excluir_categoria_bt = QPushButton('Excluir Categoria')
		self.excluir_categoria_bt.setStyleSheet(estilo_botao)
		self.excluir_categoria_bt.clicked.connect(self.excluir_categoria)
		
		main_v_box_cat = QVBoxLayout()
		main_v_box_cat.addWidget(self.adicionar_categoria_ed)
		main_v_box_cat.addWidget(self.adicionar_categoria_bt)
		main_v_box_cat.addWidget(self.categoria_combo)
		main_v_box_cat.addWidget(self.excluir_categoria_bt)
		self.setLayout(main_v_box_cat)
		
	def adicionar_combo(self):
		var = 0
		
		categoria = self.adicionar_categoria_ed.text()
		 
		#Se não tiver nada escrito na adição da categoria
		if categoria == '':
			QMessageBox.warning(self, 'Categoria deve ser informado',
			'''<p> O nome da categoria deve ser informado </p>''',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
		
		#Se tiver algo escrito, verifica a existência na lista
		if categoria != '':
			for cat in self.categoria:
				
				if categoria == cat:
					QMessageBox.warning(self, 'Categoria já existente',
					f'''Categoria '{categoria}' já existente''',
					QMessageBox.StandardButton.Ok,
					QMessageBox.StandardButton.Ok)
					self.adicionar_categoria_ed.clear()
				else:
					pass
					
				if categoria != cat:
					var += 1
		
		if var == len(self.categoria):
			self.categoria_combo.clear()
			self.categoria.append(categoria)
			self.categoria_combo.addItems(self.categoria)
			self.salvar_json()
			self.adicionar_categoria_ed.clear()
					
				
	def excluir_categoria(self):
		item_excluir = self.categoria_combo.currentText()
		
		answer = QMessageBox.warning(self, 'Excluir item',
		f'''<p> Tem certeza que deseja excluir a categoria 
		' {item_excluir} '?</p>''',
		QMessageBox.StandardButton.Yes |\
		QMessageBox.StandardButton.No,
		QMessageBox.StandardButton.No)
		
		if answer == QMessageBox.StandardButton.Yes:
			if len(self.categoria) == 0:
				pass
			
			if len(self.categoria) != 0:
				if item_excluir != '':
					self.categoria.remove(item_excluir)
					self.categoria_combo.clear()
					self.categoria_combo.addItems(self.categoria)
					self.salvar_json()
				if item_excluir == '':
					pass
		if answer == QMessageBox.StandardButton.No:
			pass
			
		
		
		
		
		
	def carregar_categoria(self):
		try:
			with open('base_data/categoria.json', 'r') as file:
				content = file.read()
				if content:
					self.categoria = (json.loads(content))
					
		except (FileNotFoundError, json.JSONDecodeError):
			pass
				
	def salvar_json(self):
		try:
			with open('base_data/categoria.json', 'w') as file:
				json.dump(self.categoria, file)
		except FileNotFoundError:
			pass		
		




