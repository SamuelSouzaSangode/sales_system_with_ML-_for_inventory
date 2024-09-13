import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton,
QGridLayout, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Sobre_(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setFixedSize(300, 600)
		self.setWindowTitle('Sobre o programa T1001')
		self.info = {}
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		botao_sobre = QPushButton('Sobre')
		botao_sobre.clicked.connect(self.sobre_set)
		
		botao_modo = QPushButton('Modo de usar')
		botao_modo.clicked.connect(self.modo_set)
		
		self.informacoes = QTextEdit()
		
		salvar = QPushButton('Salvar')
		salvar.clicked.connect(self.salvar)
		
		
		main_grid = QGridLayout()
		main_grid.addWidget(botao_sobre, 0, 0)
		main_grid.addWidget(botao_modo, 0, 1)
		main_grid.addWidget(self.informacoes, 1, 0, 1, 2)
		self.setLayout(main_grid)
	def sobre_set(self):
		self.informacoes.setText("\t O T1001 foi criado para os novos empres\u00e1rios, afim de fornecer um sistema pr\u00e1tico, simples e intuitivo para gerenciar seu estoque.\n\tEstamos felizes que voc\u00ea esteja entrando nesse grupo seleto que poucas pessoas tem a oportunidade de degustar no Brasil.\n\tAcreditamos que os recursos s\u00e3o as pernas que movimentam as ideias do mundo, gerencie seu capital com afinco e goze da vida de empres\u00e1rio que sempre sonhou!!!")
		
	def modo_set(self):
		self.informacoes.setText("1) Como fazer vendas mais r\u00e1pido\n2) Como devolver vendas\n\nObs: Sempre use n\u00fameros separados por '.' ponto e n\u00e3o por ',' v\u00edrgulas para evitar erros em seu processamento.\n\n\t1) Fazer Vendas\nO T1001 foi criado para ser mais pr\u00e1tico na hora de venda, siga os passos:\n - Clique em Venda\n\n - Clique em Nova Venda\n\n - Digite o nome do item que deseja na barra de pesquisa, aperte TAB para avan\u00e7ar nas op\u00e7\u00f5es, apertando TAB pela primeira vez, seleciona a caixa de op\u00e7\u00f5es, voc\u00ea pode clicar nela e selecionar, ou voc\u00ea pode usar as setas para cima e para baixo, ao apertar TAB pela segunda vez, voc\u00ea pode digitar a quantidade que deseja vender, ao apertar TAB pela terceira vez, voc\u00ea pode digita o valor que deseja vender o produto e apertando ENTER ou F10, lan\u00e7a  os itens.\n - Se desejar apagar o item que foi lan\u00e7ado, clique no bot\u00e3o 'X'.\n - Para finalizar a venda, ou aperte F2 ou clique no bot\u00e3o.\n - Obs: Letra mai\u00fasculas s\u00e3o levadas em considera\u00e7\u00e3o.\n - TENTE USAR O PROGRAMA DE VENDAS ASSIM, POIS FACILITAR\u00c1 A SUA VIDA QUANDO O MOVIMENTO DA SUA LOJA FOR EXCEDENTE, FOI CONSTRU\u00cdDO PARA FAZER A VENDA SEM TIRAR AS M\u00c3O DO TECLADO.\n\n\t2) Devolver Vendas\n\tVoc\u00ea vai primeiramente precisar ter em m\u00e3o o codigo da venda, ele estar\u00e1 dispon\u00edvel para voc\u00ea na p\u00e1gina de vendas como 'C\u00d3DIGO'. Siga os passos:\n\n - O primeiro passo \u00e9 digitar o item que vai ser devolvido na barra 'Pesquisar venda por item' e em seguida selecionar o item na barra de op\u00e7\u00f5es. \n\n- Clique no Bot\u00e3o 'pesquisar item vendido' e as vendas ser\u00e3o filtradas apenas com esse item vendido. Veja ent\u00e3o o C\u00d3DIGO da venda que deseja fazer a devolu\u00e7\u00e3o.\n\n - Para devolver todos os items de uma venda em uma s\u00f3 vez, digite o codigo da venda e clique em 'Cancelar venda'.\n\n- Caso voc\u00ea queira devolver apenas alguns itens e parcial, clique em 'Devolver item', uma janela abrir\u00e1 e voc\u00ea dever\u00e1 digitar o c\u00f3digo da venda, selecione o item que deseja para devolver e as suas quantidades e fa\u00e7a a devolu\u00e7\u00e3o parcial.\n\n\n\n\n")
		
	def salvar(self):
		text = self.informacoes.toPlainText()
		self.info['modo'] = text
		self.salvar_json()
	def salvar_json(self):
		try:
			with open('base_data/sobre.json', 'w') as file:
				json.dump(self.info, file)
				
		except FileNotFoundError:
			print('Deu errado')
		
	def carregar_json(self):
		try:
			with open('base_data/sobre.json', 'r') as file:
				content = file.read()
				if content:
					self.info.update(json.loads(content))
					
		except (FileNotFoundError, json.JSONDecodeError):
			pass	
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Sobre_()
	sys.exit(app.exec())
