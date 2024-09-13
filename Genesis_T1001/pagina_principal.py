import sys, json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton,
QHBoxLayout, QVBoxLayout, QStackedLayout, QTextEdit, QLineEdit,
QLabel, QCheckBox, QGridLayout, QMessageBox, QDialog, QComboBox,
QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from adicionar_item_estoque_pg import Adicionar_item_dialog
from categoria_pg import Adicionar_Categoria
from subcategoria_pg import Adicionar_sub_categoria
from remover_item_estoque_pg import Remover_item_estoque
from editar_item_estoque_pg import Editar_item_dialog
from ajustar_preco_custo_pg import Ajustar_custo_preco
from adicionar_compra_pg import Adicionar_compra
from adicionar_fornecedor_pg import Adicionar_fornecedor
from remover_fornecedor_pg import Remover_fornecedor
from editar_fornecedor_pg import Editar_fornecedor
from adicionar_cliente_pg import Adicionar_cliente
from editar_cliente_pg import Editar_cliente
from remover_cliente_pg import Remover_cliente
from divida_pg import Divida
from nova_venda_pg import Nova_venda
from devolver_venda_pg import Devolver_venda
from sobre import Sobre_
from curva_demanda import item_t_e_item_media_anual
from t1001 import T1001

'''
cor janela funfo = #2C2222
cor botao principal = #918787
cor botao principal pressionado = #D42323

'''

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		
		self.resize(400, 400)
		self.setWindowTitle('Genesis:.. T1001 - Armagedom')
		self.estoque = {}
		self.demanda ={}
		self.categoria = []
		self.subcategoria = []
		self.fornecedor = {}
		self.cliente = {}
		self.historico_vendas = {}
		self.carregar_historico_vendas()
		self.preco_sugerido_dic = {}
		self.carregar_estoque()
		self.carregar_fornecedor()
		self.carregar_cliente()
		self.setUpMainWindow()
		self.carregar_data_minima()
		self.atualizar_preco_sugerido()
		self.showMaximized()

	def setUpMainWindow(self):
		#Estilo do todos os edits
		self.ed_style = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		
		'''Parte fixa da página'''
		
		'''Fonte'''
		font = 'Arial'
		tamanho = 18
		
		'''Tamanho botao'''
		height = 30
		width = 200
		
		estilo_botao_t1001 = """
			QPushButton {background-color: #353535;
			color: red;
			border-radius: 10px;
			border: none;}
			
		QPushButton:pressed {background-color: #FFFFFF;}
			"""
		
		
		estilo_botao = """
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""
		
		self.botao_t1001 = QPushButton('T1001')
		self.botao_t1001.setFont(QFont(font, tamanho))
		self.botao_t1001.setStyleSheet(estilo_botao_t1001)
		self.botao_t1001.setFixedSize(120, 30)
		self.botao_t1001.clicked.connect(self.t1001)
		
		self.botao_venda = QPushButton('Venda')
		self.botao_venda.setFont(QFont(font, tamanho))
		self.botao_venda.setStyleSheet(estilo_botao)
		self.botao_venda.setFixedSize(80, 30)
		self.botao_venda.clicked.connect(lambda: self.troca_de_pagina(3))
		
		self.botao_devolver = QPushButton('Devolução')
		self.botao_devolver.setFont(QFont(font, tamanho))
		self.botao_devolver.setStyleSheet(estilo_botao)
		self.botao_devolver.setFixedSize(120, 30)
		
		self.botao_estoque = QPushButton('Estoque')
		self.botao_estoque.setFont(QFont(font, tamanho))
		self.botao_estoque.setStyleSheet(estilo_botao)
		self.botao_estoque.setFixedSize(100, 30)
		self.botao_estoque.clicked.connect(lambda: self.troca_de_pagina(0))
		
		self.botao_fornecedor = QPushButton('Fonecedor')
		self.botao_fornecedor.setFont(QFont(font, tamanho))
		self.botao_fornecedor.setStyleSheet(estilo_botao)
		self.botao_fornecedor.setFixedSize(120, 30)
		self.botao_fornecedor.clicked.connect(lambda: self.troca_de_pagina(1))
		
		self.botao_cliente = QPushButton('Cliente')
		self.botao_cliente.setFont(QFont(font, tamanho))
		self.botao_cliente.setStyleSheet(estilo_botao)
		self.botao_cliente.setFixedSize(80, 30)
		self.botao_cliente.clicked.connect(lambda: self.troca_de_pagina(2))
		
		self.botao_metricas = QPushButton('Métricas')
		self.botao_metricas.setFont(QFont(font, tamanho))
		self.botao_metricas.setStyleSheet(estilo_botao)
		self.botao_metricas.setFixedSize(120, 30)
		
		self.botao_ajuda = QPushButton()
		self.botao_ajuda.setStyleSheet(estilo_botao)
		self.botao_ajuda.setFixedSize(100, 30)
		icon = QIcon('base_data/ajuda.png')
		self.botao_ajuda.setIconSize(QSize(30, 30))
		self.botao_ajuda.setIcon(icon)
		self.botao_ajuda.clicked.connect(self.sobre)
		
		
		
		self.botoes_main_h_box = QHBoxLayout()
		self.botoes_main_h_box.addWidget(self.botao_t1001)
		self.botoes_main_h_box.addSpacing(60)
		self.botoes_main_h_box.addWidget(self.botao_venda)
		self.botoes_main_h_box.addSpacing(60)
		#self.botoes_main_h_box.addWidget(self.botao_devolver)
		self.botoes_main_h_box.addWidget(self.botao_estoque)
		self.botoes_main_h_box.addSpacing(60)
		self.botoes_main_h_box.addWidget(self.botao_fornecedor)
		self.botoes_main_h_box.addSpacing(60)
		self.botoes_main_h_box.addWidget(self.botao_cliente)
		self.botoes_main_h_box.addSpacing(60)
		#self.botoes_main_h_box.addWidget(self.botao_metricas)
		self.botoes_main_h_box.addWidget(self.botao_ajuda)
		self.botoes_main_h_box.setAlignment(Qt.AlignmentFlag.AlignTop)
		
		botoes_container = QWidget()
		botoes_container.setLayout(self.botoes_main_h_box)

# PÁGINA DE ESTOQUE ####################################################
		
		font_estoque = 'Arial'
		tamanho_estoque = 18
		
		'''Tamanho botao'''
		height_estoque = 30
		width_estoque = 300
		
		
		estilo_botao_estoque = """
			QPushButton {background-color: #DBD4D4; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""
		#Adiciona um novo item ao estoque
		self.adicionar_botao = QPushButton('Adicionar novo item')
		self.adicionar_botao.setFont(QFont(font, tamanho))
		self.adicionar_botao.setStyleSheet(
		estilo_botao_estoque)
		self.adicionar_botao.setMaximumHeight(height_estoque)
		self.adicionar_botao.setMaximumWidth(width_estoque)
		self.adicionar_botao.clicked.connect(self.adicionar_item)
		
		
		#Remove um item do estoque
		self.remover_botao = QPushButton('Remover item do estoque')
		self.remover_botao.setFont(QFont(
		font_estoque, tamanho_estoque))
		self.remover_botao.setStyleSheet(
		estilo_botao_estoque)
		self.remover_botao.setMaximumHeight(height_estoque)
		self.remover_botao.setMaximumWidth(width_estoque)
		self.remover_botao.clicked.connect(self.remover_item)
		
		#Editar item
		self.editar_item_botao = QPushButton('Editar item')
		self.editar_item_botao.setFont(
		QFont(font_estoque, tamanho_estoque))
		self.editar_item_botao.setStyleSheet(
		estilo_botao_estoque)
		self.editar_item_botao.setMaximumHeight(height_estoque)
		self.editar_item_botao.setMaximumWidth(width_estoque)
		self.editar_item_botao.clicked.connect(self.editar_item)
		
		#Ajustar Preço/Custo de forma geral
		self.ajustar_valor_botao = QPushButton('Ajustar Preço/Custo')
		self.ajustar_valor_botao.setFont(
		QFont(font_estoque, tamanho_estoque))
		self.ajustar_valor_botao.setStyleSheet(
		estilo_botao_estoque)
		self.ajustar_valor_botao.setMaximumHeight(height_estoque)
		self.ajustar_valor_botao.setMaximumWidth(width_estoque)
		self.ajustar_valor_botao.clicked.connect(self.ajustar_custo_preco)
		
		#Adicionar compra
		self.adicionar_compra_botao = QPushButton('Adicionar compra')
		self.adicionar_compra_botao.setFont(
		QFont(font_estoque, tamanho_estoque))
		self.adicionar_compra_botao.setStyleSheet(
		estilo_botao_estoque)
		self.adicionar_compra_botao.setMaximumHeight(height_estoque)
		self.adicionar_compra_botao.setMaximumWidth(width_estoque)
		self.adicionar_compra_botao.clicked.connect(self.adicionar_compra)
		
		#Categoria
		self.categoria_botao = QPushButton('Categoria')
		self.categoria_botao.setFont(
		QFont(font_estoque, tamanho_estoque))
		self.categoria_botao.setStyleSheet(
		estilo_botao_estoque)
		self.categoria_botao.setMaximumHeight(height_estoque)
		self.categoria_botao.setMaximumWidth(width_estoque)
		self.categoria_botao.clicked.connect(self.adicionar_categoria)
		
		#Subcategoria 
		self.subcategoria_botao = QPushButton('SubCategoria')
		self.subcategoria_botao.setFont(
		QFont(font_estoque, tamanho_estoque))
		self.subcategoria_botao.setStyleSheet(
		estilo_botao_estoque)
		self.subcategoria_botao.setMaximumHeight(height_estoque)
		self.subcategoria_botao.setMaximumWidth(width_estoque)
		self.subcategoria_botao.clicked.connect(self.adicionar_sub_categoria)
		
		#Pesquisa item no estoque
		self.pesquisa_estoque = QLineEdit()
		self.pesquisa_estoque.setFont(QFont('Arial', 14))
		self.pesquisa_estoque.setPlaceholderText('Pesquisar item...')
		self.pesquisa_estoque.setClearButtonEnabled(True)
		self.pesquisa_estoque.setMaximumWidth(500)
		self.pesquisa_estoque.setStyleSheet(self.ed_style)
		self.pesquisa_estoque.textEdited.connect(self.pesquisa)
		
		#Mostra os itens no estoque e sua epecificações
		self.tabela_estoque = QTableWidget(10, 10)
		self.tabela_estoque.setStyleSheet(self.ed_style)
		self.tabela_estoque.setFont(QFont('Arial', 10))
		
		
		self.quantidade_itens_label = QLabel()
		self.quantidade_itens_label.setFont(QFont('Arial', 14))
		self.quantidade_itens_label.setAlignment(
		Qt.AlignmentFlag.AlignLeft)
			
		self.valor_estoque = QLabel()
		self.valor_estoque.setFont(QFont('Arial', 12))
		self.valor_estoque.setText(f'Custo: R$ ****** / Preço: R$ ******')
		self.valor_estoque.setAlignment(
		Qt.AlignmentFlag.AlignRight)
		
		
		
		#Oculta o valor total do estoque
		self.ocultar_valores_cb = QCheckBox('Ocultar Custo/Valor')
		self.ocultar_valores_cb.toggle()
		self.ocultar_valores_cb.toggled.connect(self.valor_custo_estoque)
		
		#Comandos para serem feitos ao iniciar o programa
		self.quantidade_itens()
		self.pesquisa()
		
		
		
		'''Todas Colunas da pagina estoque'''
		self.grid_estoque_pg = QGridLayout()
		self.grid_estoque_pg.addWidget(self.adicionar_botao,0,0)
		self.grid_estoque_pg.addWidget(self.remover_botao,1,0)
		self.grid_estoque_pg.addWidget(self.editar_item_botao,2,0)
		self.grid_estoque_pg.addWidget(self.ajustar_valor_botao,3,0)
		self.grid_estoque_pg.addWidget(self.adicionar_compra_botao,4,0)
		self.grid_estoque_pg.addWidget(self.categoria_botao, 5, 0)
		self.grid_estoque_pg.addWidget(self.subcategoria_botao, 6, 0)
		self.grid_estoque_pg.addWidget(self.pesquisa_estoque,7,0)
		self.grid_estoque_pg.addWidget(self.ocultar_valores_cb,8,0)
		self.grid_estoque_pg.addWidget(self.tabela_estoque,9,0)
		self.grid_estoque_pg.addWidget(self.valor_estoque,10,0)
		self.grid_estoque_pg.addWidget(self.quantidade_itens_label, 11, 0)
		
		
		
		
		grid_estoque_container = QWidget()
		grid_estoque_container.setLayout(self.grid_estoque_pg)
		
		
# PÁGINA DE FORNECEDOR #################################################
		font_forn = 'Arial'
		tam_forn = 18
		
		'''Tamanho botao'''
		height_forn = 30
		width_forn = 300
		
		estilo_botao_forn = """
			QPushButton {background-color: #DBD4D4; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""
		
		#Adicionar um novo fonecedor e suas informações
		self.adicionar_forn_botao = QPushButton('Adicionar Fornecedor')
		self.adicionar_forn_botao.setFont(QFont(font_forn, tam_forn))
		self.adicionar_forn_botao.setStyleSheet(estilo_botao_forn)
		self.adicionar_forn_botao.setMaximumHeight(height_forn)
		self.adicionar_forn_botao.setMaximumWidth(width_forn)
		self.adicionar_forn_botao.clicked.connect(self.adicionar_fornecedor)
		
		#Edita as informações do fornecedor
		self.editar_forn_botao = QPushButton('Editar Fornecedor')
		self.editar_forn_botao.setFont(QFont(font_forn, tam_forn))
		self.editar_forn_botao.setStyleSheet(estilo_botao_forn)
		self.editar_forn_botao.setMaximumHeight(height_forn)
		self.editar_forn_botao.setMaximumWidth(width_forn)
		self.editar_forn_botao.clicked.connect(self.editar_fornecedor)
		
		#Remover fornecedor do banco de dados
		self.remover_forn_botao = QPushButton('Remover Fornecedor')
		self.remover_forn_botao.setFont(QFont(font_forn, tam_forn))
		self.remover_forn_botao.setStyleSheet(estilo_botao_forn)
		self.remover_forn_botao.setMaximumHeight(height_forn)
		self.remover_forn_botao.setMaximumWidth(width_forn)	
		self.remover_forn_botao.clicked.connect(self.remover_fornecedor)
		
		#Barra de pesquisa de fornecedores
		self.pesquisa_forn_ed = QLineEdit()
		self.pesquisa_forn_ed.setFont(QFont('Arial', 14))
		self.pesquisa_forn_ed.setPlaceholderText('Pesquisar item...')
		self.pesquisa_forn_ed.setClearButtonEnabled(True)
		self.pesquisa_forn_ed.setMaximumWidth(500)
		self.pesquisa_forn_ed.setStyleSheet(self.ed_style)	
		self.pesquisa_forn_ed.textEdited.connect(self.forn_tedit_set)
		
		#Mostra os fornecedores e informações
		self.tabela_fornecedor = QTableWidget()
		self.tabela_fornecedor.setStyleSheet(self.ed_style)
		self.tabela_fornecedor.setFont(QFont('Arial', 10))	
		self.forn_tedit_set()
		
		self.grid_forn_pg = QGridLayout()
		self.grid_forn_pg.addWidget(self.adicionar_forn_botao, 1, 0)
		self.grid_forn_pg.addWidget(self.editar_forn_botao, 2, 0)
		self.grid_forn_pg.addWidget(self.remover_forn_botao, 3, 0)
		self.grid_forn_pg.addWidget(self.pesquisa_forn_ed, 4, 0)
		self.grid_forn_pg.addWidget(self.tabela_fornecedor, 5, 0)	
		
		grid_forn_container = QWidget()
		grid_forn_container.setLayout(self.grid_forn_pg)
		
		
# PÁGINA DE CLIENTE ####################################################		
		font_cliente = 'Arial'
		tam_cliente = 18
		
		'''Tamanho botao'''
		height_cliente = 30
		width_cliente = 300
		
		estilo_botao_cliente = """
			QPushButton {background-color: #DBD4D4; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""		
		
		#Adicionar um novo cliente e suas informações
		self.adicionar_cliente_botao = QPushButton('Adicionar Cliente')
		self.adicionar_cliente_botao.setFont(QFont(font_cliente, tam_cliente))
		self.adicionar_cliente_botao.setStyleSheet(estilo_botao_cliente)
		self.adicionar_cliente_botao.setMaximumHeight(height_cliente)
		self.adicionar_cliente_botao.setMaximumWidth(width_cliente)
		self.adicionar_cliente_botao.clicked.connect(self.adicionar_cliente)
		
		#Edita as informações do cliente
		self.editar_cliente_botao = QPushButton('Editar Cliente')
		self.editar_cliente_botao.setFont(QFont(font_cliente, tam_cliente))
		self.editar_cliente_botao.setStyleSheet(estilo_botao_cliente)
		self.editar_cliente_botao.setMaximumHeight(height_cliente)
		self.editar_cliente_botao.setMaximumWidth(width_cliente)
		self.editar_cliente_botao.clicked.connect(self.editar_cliente)
		
		#Remover fornecedor do banco de dados
		self.remover_cliente_botao = QPushButton('Remover Cliente')
		self.remover_cliente_botao.setFont(QFont(font_cliente, tam_cliente))
		self.remover_cliente_botao.setStyleSheet(estilo_botao_cliente)
		self.remover_cliente_botao.setMaximumHeight(height_cliente)
		self.remover_cliente_botao.setMaximumWidth(width_cliente)	
		self.remover_cliente_botao.clicked.connect(self.remover_cliente)
		
		#Adicionar divida cliente
		self.ad_divida_botao = QPushButton('Dívida')
		self.ad_divida_botao.setFont(QFont(font_cliente, tam_cliente))
		self.ad_divida_botao.setStyleSheet(estilo_botao_cliente)
		self.ad_divida_botao.setMaximumHeight(height_cliente)
		self.ad_divida_botao.setMaximumWidth(width_cliente)
		self.ad_divida_botao.clicked.connect(self.divida)
		
		
		
		
		#Barra de pesquisa de Clientes
		self.pesquisa_cliente_ed = QLineEdit()
		self.pesquisa_cliente_ed.setFont(QFont('Arial', 14))
		self.pesquisa_cliente_ed.setPlaceholderText('Pesquisar cliente...')
		self.pesquisa_cliente_ed.setClearButtonEnabled(True)
		self.pesquisa_cliente_ed.setMaximumWidth(500)
		self.pesquisa_cliente_ed.setStyleSheet(self.ed_style)	
		self.pesquisa_cliente_ed.textEdited.connect(self.cliente_tedit_set)	
			
		
		#Mostra os clientes e informações
		self.cliente_tabela = QTableWidget()
		self.cliente_tabela.setStyleSheet(self.ed_style)
		self.cliente_tabela.setFont(QFont('Arial', 10))	
		self.cliente_tedit_set()		
		
		
		
		
		self.grid_cliente_pg = QGridLayout()
		self.grid_cliente_pg.addWidget(self.adicionar_cliente_botao, 1, 0)
		self.grid_cliente_pg.addWidget(self.editar_cliente_botao, 2, 0)
		self.grid_cliente_pg.addWidget(self.remover_cliente_botao, 3, 0)
		self.grid_cliente_pg.addWidget(self.ad_divida_botao, 4, 0)
		self.grid_cliente_pg.addWidget(self.pesquisa_cliente_ed, 5,0)
		self.grid_cliente_pg.addWidget(self.cliente_tabela, 6, 0)	
		
		grid_cliente_container = QWidget()
		grid_cliente_container.setLayout(self.grid_cliente_pg)		
		
# PÁGINA DE VENDA #####################################################
		font_venda = 'Arial'
		tam_venda = 18
		
		'''Tamanho botao'''
		height_venda = 30
		width_venda = 300
		
		estilo_botao_venda = """
			QPushButton {background-color: #DBD4D4; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		"""		
		desenvolvedor_label = QLabel()
		desenvolvedor_label.setText('Desenvolvedor: Samuel Souza Santos')
		
		self.situacao_atualizacao = QLabel('Situação:---')
		self.situacao_atualizacao.setFont(QFont('Arial', 12))

		nova_venda_botao = QPushButton('Nova Venda')
		nova_venda_botao.setFont(QFont(font_venda, tam_venda))
		nova_venda_botao.setStyleSheet(estilo_botao_venda)
		nova_venda_botao.setMaximumHeight(height_venda)
		nova_venda_botao.setMaximumWidth(width_venda)	
		nova_venda_botao.clicked.connect(self.nova_venda)
		
		#Inserir o código da venda
		self.codigo_venda_ed = QLineEdit()
		self.codigo_venda_ed.setFont(QFont('Arial', 14))
		self.codigo_venda_ed.setPlaceholderText('Código da venda para cancelar...')
		self.codigo_venda_ed.setClearButtonEnabled(True)
		self.codigo_venda_ed.setMaximumWidth(width_venda)
		self.codigo_venda_ed.setStyleSheet(self.ed_style)	
		#self.codigo_venda_ed.textEdited.connect(self.cliente_tedit_set)
		
		#Pesquisa a venda através de itens
		self.pesquisa_item_ed = QLineEdit()
		self.pesquisa_item_ed.setFont(QFont('Arial', 14))
		self.pesquisa_item_ed.setPlaceholderText('Pesquisar venda por item...')
		self.pesquisa_item_ed.setClearButtonEnabled(True)
		#self.pesquisa_item_ed.setMaximumWidth(500)
		self.pesquisa_item_ed.setStyleSheet(self.ed_style)
		#self.pesquisa_item_ed.textEdited.connect(self.historico_vendas_tedit_set)
		self.pesquisa_item_ed.textEdited.connect(self.pesquisa_combo_historico_vendas)
		
		#Data minima para a analise de dados
		self.data_minima_ed = QLineEdit()
		self.data_minima_ed.setFont(QFont('Arial', 14))
		self.data_minima_ed.setPlaceholderText('Data minima   (dd-mm-yy)...')
		self.data_minima_ed.setClearButtonEnabled(True)
		self.data_minima_ed.setStyleSheet(self.ed_style)
		self.data_minima_ed.textEdited.connect(self.salvar_data_minima)
		
		
		self.item_pesquisa_combo = QComboBox()
		self.item_pesquisa_combo.setFont(QFont('Arial', 14))
		#self.item_pesquisa_combo.setMaximumWidth(500)
		self.item_pesquisa_combo.setStyleSheet(self.ed_style)


		self.botao_pesquisa_item = QPushButton('Pesquisar item vendido')
		self.botao_pesquisa_item.setFont(QFont(font_venda, tam_venda))
		self.botao_pesquisa_item.setStyleSheet(estilo_botao_venda)
		self.botao_pesquisa_item.clicked.connect(self.historico_vendas_tedit_set)

		
		editar_venda_botao = QPushButton('Editar Venda')
		editar_venda_botao.setFont(QFont(font_venda, tam_venda))
		editar_venda_botao.setStyleSheet(estilo_botao_venda)
		editar_venda_botao.setMaximumHeight(height_venda)
		editar_venda_botao.setMaximumWidth(width_venda)	
		#editar_venda_botao.clicked.connect(self.remover_venda)
		
		devolver_item_botao = QPushButton('Devolver Item')
		devolver_item_botao.setFont(QFont(font_venda, tam_venda))
		devolver_item_botao.setStyleSheet(estilo_botao_venda)
		devolver_item_botao.setMaximumHeight(height_venda)
		devolver_item_botao.setMaximumWidth(width_venda)	
		devolver_item_botao.clicked.connect(self.devolver_venda)
		
		cancelar_venda_botao = QPushButton('Cancelar Venda')
		cancelar_venda_botao.setFont(QFont(font_venda, tam_venda))
		cancelar_venda_botao.setStyleSheet(estilo_botao_venda)
		cancelar_venda_botao.setMaximumHeight(height_venda)
		cancelar_venda_botao.setMaximumWidth(width_venda)	
		cancelar_venda_botao.clicked.connect(self.cancelar_venda)
		
		preco_sugerido_botao = QPushButton('Atualizar Preco Sug.')
		preco_sugerido_botao.setFont(QFont(font_venda, tam_venda))
		preco_sugerido_botao.setStyleSheet(estilo_botao_venda)
		preco_sugerido_botao.setMaximumHeight(height_venda)
		preco_sugerido_botao.setMaximumWidth(width_venda)
		preco_sugerido_botao.clicked.connect(self.atualizar_preco_sugerido)
		
		aprendizado_t1001 = QPushButton('Atualizar T1001 Análise')
		aprendizado_t1001.setFont(QFont(font_venda, tam_venda))
		aprendizado_t1001.setStyleSheet(estilo_botao_venda)
		aprendizado_t1001.setMaximumWidth(width_venda)
		aprendizado_t1001.clicked.connect(self.atualizar_t1001___)
		
		
		self.historico_venda = QTextEdit()	
		his_venda_label = QLabel('Histórico de vendas')
		his_venda_label.setFont(QFont('Arial', 14))
		
		self.faturamento_lucro_dia = QTextEdit()
		fat_lucro_dia_label = QLabel('Faturamento - Lucro (Diário)')
		fat_lucro_dia_label.setFont(QFont('Arial', 14))
		
		self.faturamento_lucro_mes = QTextEdit()
		fat_lucro_mes_label = QLabel('Faturamento - Lucro (Mês)')
		fat_lucro_mes_label.setFont(QFont('Arial', 14))
		
		self.faturamento_lucro_ano = QTextEdit()	
		fat_lucro_ano_label = QLabel('Faturamento - Lucro (Ano)')
		fat_lucro_ano_label.setFont(QFont('Arial', 14))
		
		main_grid_venda_pg = QGridLayout()
		main_grid_venda_pg.addWidget(nova_venda_botao, 1, 1)
		main_grid_venda_pg.addWidget(self.codigo_venda_ed, 2, 2)
		main_grid_venda_pg.addWidget(editar_venda_botao, 2, 5)
		main_grid_venda_pg.addWidget(devolver_item_botao, 2, 4)
		main_grid_venda_pg.addWidget(cancelar_venda_botao, 2, 3)
		main_grid_venda_pg.addWidget(self.data_minima_ed, 3, 4)
		main_grid_venda_pg.addWidget(preco_sugerido_botao, 3, 5)
		#main_grid_venda_pg.addWidget(self.situacao_atualizacao,4, 4, alignment=Qt.AlignmentFlag.AlignCenter)
		main_grid_venda_pg.addWidget(aprendizado_t1001,4, 5)
		main_grid_venda_pg.addWidget(self.pesquisa_item_ed, 3, 1, 1, 2)
		main_grid_venda_pg.addWidget(self.item_pesquisa_combo, 4, 1, 1, 2)
		main_grid_venda_pg.addWidget(self.botao_pesquisa_item, 5, 1, 1, 2)
		main_grid_venda_pg.addWidget(his_venda_label, 6, 1)
		main_grid_venda_pg.addWidget(self.historico_venda,7,1,1,2)
		main_grid_venda_pg.addWidget(fat_lucro_dia_label, 6, 3)
		main_grid_venda_pg.addWidget(self.faturamento_lucro_dia,7, 3, 1, 1)
		main_grid_venda_pg.addWidget(fat_lucro_mes_label, 6, 4)
		main_grid_venda_pg.addWidget(self.faturamento_lucro_mes,7, 4, 1, 1)
		main_grid_venda_pg.addWidget(fat_lucro_ano_label, 6, 5)
		main_grid_venda_pg.addWidget(self.faturamento_lucro_ano, 7, 5, 1, 1)
		main_grid_venda_pg.addWidget(desenvolvedor_label, 8, 5, 1, 2)
		
		grid_venda_container = QWidget()
		grid_venda_container.setLayout(main_grid_venda_pg)
		
		
		
		
		#Criando o StackedLayout
		self.stacked_layout = QStackedLayout()
		self.stacked_layout.addWidget(grid_estoque_container)
		self.stacked_layout.addWidget(grid_forn_container)
		self.stacked_layout.addWidget(grid_cliente_container)
		self.stacked_layout.addWidget(grid_venda_container)

		
		
		#Criando o layout principal
		main_v_box = QVBoxLayout()
		main_v_box.addWidget(botoes_container)
		main_v_box.addLayout(self.stacked_layout)
		self.setLayout(main_v_box)
		self.diario_tedit_set()
		self.mes_tedit_set()
		self.ano_tedit_set()
		
	def troca_de_pagina(self, index):
		
		self.stacked_layout.setCurrentIndex(index)
		self.carregar_estoque()
		self.carregar_fornecedor()
		self.carregar_cliente()
		self.quantidade_itens()
		self.atualizar_preco_sugerido()
		
		self.pesquisa()#Seta a tabela que mostra os itens do estoque
		self.forn_tedit_set()
		self.cliente_tedit_set()
		self.carregar_historico_vendas()
		self.historico_vendas_tedit_set()
		self.diario_tedit_set()
		self.mes_tedit_set()
		self.ano_tedit_set()
	
# Funções página ESTOQUE	
	def carregar_estoque(self):
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu estoque')
			
	def carregar_fornecedor(self):
		try:
			with open('base_data/fornecedor.json', 'r') as file:
				content = file.read()
				if content:
					self.fornecedor.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu fornecedor')	
	
	def carregar_cliente(self):
		try:
			with open('base_data/cliente.json', 'r') as file:
				content = file.read()
				if content:
					self.cliente.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu cliente')	
	
	def carregar_historico_vendas(self):
		try:
			with open('base_data/historico_vendas.json', 'r') as file:
				content = file.read()
				if content:
					self.historico_vendas.update(json.loads(content))
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas não encontrado')	
			
	def carregar_data_minima(self):
		with open('base_data/data_minima.txt', 'r') as file:
			texto = file.read()
			self.data_minima_ed.setText(texto)
			
	
	def salvar_historico_vendas_json(self):
		with open('base_data/historico_vendas.json', 'w') as file:
			json.dump(self.historico_vendas, file)	
	
	def salvar_estoque(self):
		with open('base_data/estoque.json', 'w') as file:
			json.dump(self.estoque, file)	
			
	def salvar_preco_sugerido(self):
		with open('base_data/preco_sugerido.json', 'w') as file:
			json.dump(self.preco_sugerido_dic, file)
			
	def salvar_data_minima(self):
		with open('base_data/data_minima.txt', 'w') as file:
			file.write(self.data_minima_ed.text())
			
	
	def pesquisa(self):
		self.pesquisados = []
		texto = self.pesquisa_estoque.text()
		if texto != '':
			for item, info in self.estoque.items():
				if texto in item:
					self.pesquisados.append(item)
		if texto == '':
			self.tabela_estoque.clear()
			for item in list(self.estoque.keys()):
				self.pesquisados.append(item)
					
		self.estoque_tabela_set()		
	
	def estoque_tabela_set(self):
		
		self.tabela_estoque.clear()
		lista_cabecalho = ['Código', 'Produto', 'Preço', 
			'Custo', 'Quantidade', 'Categoria', 'SubCategoria',
			'Marca', 'Fonecedor']
		
		var_coluna = 0	
		for nome in lista_cabecalho:
			self.tabela_estoque.setHorizontalHeaderItem(
				var_coluna, QTableWidgetItem(nome))
			var_coluna += 1
		
		linhas = len(self.pesquisados)
		colunas = 9
		self.tabela_estoque.setRowCount(linhas)
		self.tabela_estoque.setColumnCount(colunas)
		
		
		
		var_linha = 0	
		for item in self.pesquisados:
			#Codigo 
			self.tabela_estoque.setItem(
				var_linha, 0, QTableWidgetItem(
					self.estoque[item]['codigo']))
					
			#Produto
			self.tabela_estoque.setItem(
				var_linha, 1, QTableWidgetItem(item))
				
			#Preço
			self.tabela_estoque.setItem(
				var_linha, 2, QTableWidgetItem(
				f"R$ {self.estoque[item]['valor']}"))
				
			#Custo 
			self.tabela_estoque.setItem(
				var_linha, 3, QTableWidgetItem(
				f"R$ {self.estoque[item]['custo']}"))
				
			#Quantidade
			self.tabela_estoque.setItem(
				var_linha, 4, QTableWidgetItem(
				f"{self.estoque[item]['quantidade']}"))
				
			#Categoria 
			self.tabela_estoque.setItem(
				var_linha, 5, QTableWidgetItem(
				self.estoque[item]['categoria']))
			
			#SubCategoria
			self.tabela_estoque.setItem(
				var_linha, 6, QTableWidgetItem(
				self.estoque[item]['subcategoria']))
				
			#Marca
			self.tabela_estoque.setItem(
				var_linha, 7, QTableWidgetItem(
				self.estoque[item]['marca']))
				
			#Fornecedor
			self.tabela_estoque.setItem(
				var_linha, 8, QTableWidgetItem(
				self.estoque[item]['fornecedor']))
					
					
			var_linha += 1
		self.tabela_estoque.resizeColumnsToContents()
		largura = 100
		self.tabela_estoque.horizontalHeader().resizeSection(1, 400)
		self.tabela_estoque.horizontalHeader().resizeSection(2, largura)
		self.tabela_estoque.horizontalHeader().resizeSection(3, largura)
		self.tabela_estoque.horizontalHeader().resizeSection(4, largura)
		self.tabela_estoque.horizontalHeader().resizeSection(5, largura)
		self.tabela_estoque.horizontalHeader().resizeSection(6, largura)
		self.tabela_estoque.horizontalHeader().resizeSection(7, largura)
						
	
	
	def forn_tedit_set(self):
		self.tabela_fornecedor.clear()
		self.carregar_fornecedor()
		#Especificando o cabeçado e a tabela
		linhas = len(list(self.fornecedor.keys()))
		self.tabela_fornecedor.setColumnCount(6)
		self.tabela_fornecedor.setRowCount(linhas)
			
		cabecalhos = ['Fornecedor', 'Telefone 1', 
				'Telefone 2', 'Email', 'Endereço', 
				'Fornecedor']
		coluna = 0
		for c in cabecalhos:
			self.tabela_fornecedor.setHorizontalHeaderItem(
				coluna, QTableWidgetItem(c))
			coluna +=1
		
		
		#Verificando as pesquisa
		if self.pesquisa_forn_ed.text() == '':
			var = 0
			for forn, info in self.fornecedor.items():
				self.tabela_fornecedor.setItem(
					var, 0, QTableWidgetItem(forn))
				
				self.tabela_fornecedor.setItem(
					var, 1, QTableWidgetItem(info['telefone_1']))
					
				self.tabela_fornecedor.setItem(
					var, 2, QTableWidgetItem(info['telefone_2']))
					
				self.tabela_fornecedor.setItem(
					var, 3, QTableWidgetItem(info['email']))
				
				self.tabela_fornecedor.setItem(
					var, 4, QTableWidgetItem(info['endereco']))
					
				self.tabela_fornecedor.setItem(
					var, 5, QTableWidgetItem(info['forn']))
					
				var += 1
				
			self.tabela_estoque.resizeColumnsToContents()
			largura = 100
			self.tabela_estoque.horizontalHeader().resizeSection(1, 400)
			self.tabela_estoque.horizontalHeader().resizeSection(2, largura)
			self.tabela_estoque.horizontalHeader().resizeSection(3, largura)
			self.tabela_estoque.horizontalHeader().resizeSection(4, largura)
			self.tabela_estoque.horizontalHeader().resizeSection(5, largura)
			self.tabela_estoque.horizontalHeader().resizeSection(6, largura)
			self.tabela_estoque.horizontalHeader().resizeSection(7, largura)
				
				
				
				
				
			
				
			
		
		else:

			var = 0
			for forn, info in self.fornecedor.items():
				if self.pesquisa_forn_ed.text() in forn:
					self.tabela_fornecedor.setItem(
						var, 0, QTableWidgetItem(forn))
						
					self.tabela_fornecedor.setItem(
						var, 1, QTableWidgetItem(info['telefone_1']))
					
					self.tabela_fornecedor.setItem(
						var, 2, QTableWidgetItem(info['telefone_2']))
					
					self.tabela_fornecedor.setItem(
						var, 3, QTableWidgetItem(info['email']))
				
					self.tabela_fornecedor.setItem(
						var, 4, QTableWidgetItem(info['endereco']))
					
					self.tabela_fornecedor.setItem(
						var, 5, QTableWidgetItem(info['forn']))
					var += 1
						
		
	def cliente_tedit_set(self):
		self.cliente_tabela.clear()
		
		linhas = len(list(self.cliente.keys()))
		self.cliente_tabela.setColumnCount(7)
		self.cliente_tabela.setRowCount(linhas)
			
		cabecalhos = ['Cliente', 'Telefone 1', 
				'Telefone 2', 'Email', 'Endereço', 
				'Atividade', 'Dívida']
		coluna = 0
		for c in cabecalhos:
			self.cliente_tabela.setHorizontalHeaderItem(
				coluna, QTableWidgetItem(c))
			coluna +=1		
		
		var = 0
		if self.pesquisa_cliente_ed.text() == '':
			for cliente, info in self.cliente.items():
				self.cliente_tabela.setItem(
					var, 0, QTableWidgetItem(cliente))
				
				self.cliente_tabela.setItem(
					var, 1, QTableWidgetItem(info['telefone_1']))
					
				self.cliente_tabela.setItem(
					var, 2, QTableWidgetItem(info['telefone_2']))
					
				self.cliente_tabela.setItem(
					var, 3, QTableWidgetItem(info['email']))
					
				self.cliente_tabela.setItem(
					var, 4, QTableWidgetItem(info['endereco']))
					
				self.cliente_tabela.setItem(
					var, 5, QTableWidgetItem(info['atividade']))
				
				self.cliente_tabela.setItem(
					var, 6, QTableWidgetItem(str(info['divida'])))
					
				var += 1
				
			self.cliente_tabela.resizeColumnsToContents()
				
				
			
				
			
		
		else:
			for cliente, info in self.cliente.items():
				if self.pesquisa_cliente_ed.text() in cliente:
					self.cliente_tabela.setItem(
						var, 0, QTableWidgetItem(cliente))
				
					self.cliente_tabela.setItem(
						var, 1, QTableWidgetItem(info['telefone_1']))
					
					self.cliente_tabela.setItem(
						var, 2, QTableWidgetItem(info['telefone_2']))
					
					self.cliente_tabela.setItem(
						var, 3, QTableWidgetItem(info['email']))
					
					self.cliente_tabela.setItem(
						var, 4, QTableWidgetItem(info['endereco']))
					
					self.cliente_tabela.setItem(
						var, 5, QTableWidgetItem(info['atividade']))
				
					self.cliente_tabela.setItem(
						var, 6, QTableWidgetItem(str(info['divida'])))
					
					var += 1
				
				self.cliente_tabela.resizeColumnsToContents()			
					
	
	#Item selecionado no self.item_pesquisa_combo mostra a venda que contem esse item	
	def historico_vendas_tedit_set(self):
		item_combo = self.item_pesquisa_combo.currentText()
		
		self.historico_venda.clear()
		if item_combo == '':
			for codigo, dic in self.historico_vendas.items():
				valor = 0
				
				codigo_f = '{:<60}'.format(codigo)
				self.historico_venda.append(f'CÓDIGO: {codigo_f}')
				
				for item, info in dic['itens'].items():
					valor += info['quantidade'] * info['valor']
					item_f = '{:<50}'.format(item)
					self.historico_venda.append(f'- x{info["quantidade"]}   R${info["valor"]}      {item_f}')
				valor_form = round(valor, 2)
				self.historico_venda.append(f'**Total = R${valor_form}')
				
				data = dic['info']['data']
				mes = dic['info']['mes']
				dia = dic['info']['dia']
				self.historico_venda.append(f'({data})  {mes} _ {dia}')
				self.historico_venda.append('')
				self.historico_venda.append('')
		
		if item_combo != '':
			for codigo, dic in self.historico_vendas.items():
				if item_combo in dic['itens']:
					valor = 0
				
					codigo_f = '{:<60}'.format(codigo)
					self.historico_venda.append(f'CÓDIGO: {codigo_f}')
				
					for item, info in dic['itens'].items():
						valor += info['quantidade'] * info['valor']
						item_f = '{:<50}'.format(item)
						self.historico_venda.append(f'- x{info["quantidade"]}   R${info["valor"]}      {item_f}')
					valor_form = round(valor, 2)
					self.historico_venda.append(f'**Total = R${valor_form}')
				
					data = dic['info']['data']
					mes = dic['info']['mes']
					dia = dic['info']['dia']
					self.historico_venda.append(f'({data})  {mes} _ {dia}')
					self.historico_venda.append('')
					self.historico_venda.append('')
		
	def diario_tedit_set(self):
		self.faturamento_lucro_dia.clear()
		datas_diarias = []
		datas_fat_cust_lucr = {}
		for codigo, value in self.historico_vendas.items():
			if value['info']['data'] not in datas_diarias:
				datas_diarias.append(value['info']['data'])
			if value['info']['data'] in datas_diarias:
				pass
		for datas in datas_diarias:
			info = {}
			faturamento_data = 0
			custo_data = 0
			lucro_data = 0
			
			#Calcula o faturamento da data
			for codigo, value in self.historico_vendas.items():
				if value['info']['data'] == datas:
					for item, info_item in value['itens'].items():
						quantidade_vendida = self.historico_vendas[codigo]['itens'][item]['quantidade']
						valor_vendido = self.historico_vendas[codigo]['itens'][item]['valor']
						faturamento_venda = quantidade_vendida * valor_vendido
						faturamento_data += faturamento_venda
			
			#Calcula o custo e o lucro de cada data
			for codigo, value in self.historico_vendas.items():
				if value['info']['data'] == datas:
					for item, info_item in value['itens'].items():
						quantidade_vendida = self.historico_vendas[codigo]['itens'][item]['quantidade']
						custo_vendido = self.historico_vendas[codigo]['itens'][item]['custo']
						custo_venda = quantidade_vendida * custo_vendido
						custo_data += custo_venda
						lucro_data = (faturamento_data - custo_data)
						
			faturamento_data_form = round(faturamento_data, 2)	
			custo_data_form = round(custo_data, 2)
			lucro_data_form = round(lucro_data, 2)
			
			info['faturamento'] = faturamento_data_form
			info['custo'] = custo_data_form
			info['lucro'] = lucro_data_form
			datas_fat_cust_lucr[datas] = info
		

			self.faturamento_lucro_dia.append(f'Data: {datas}')
			self.faturamento_lucro_dia.append(f'Faturamento:   R${str(faturamento_data_form)}')
			self.faturamento_lucro_dia.append(f'Lucro: R${str(lucro_data_form)}')
			self.faturamento_lucro_dia.append('')
					
	def	mes_tedit_set(self):
		self.faturamento_lucro_mes.clear()
		datas_mes_ano = []
		#Adiciona as datas na lista
		for codigo, value in self.historico_vendas.items():
			if value['info']['mes_ano'] not in datas_mes_ano:
				datas_mes_ano.append(self.historico_vendas[codigo]['info']['mes_ano'])
			if value['info']['mes_ano'] in datas_mes_ano:
				pass
		
		for datas_mes in datas_mes_ano:
			faturamento = 0
			custo = 0
			lucro = 0
			for codigo, value in self.historico_vendas.items():
				if value['info']['mes_ano'] == datas_mes:
					for item, info_item in value['itens'].items():
						quantidade = info_item['quantidade']
						valor_vendido = info_item['valor']
						total_item = quantidade * valor_vendido
						faturamento += total_item
					
					for item, info_item in value['itens'].items():
						quantidade = info_item['quantidade']
						valor_vendido = info_item['custo']
						custo_item = quantidade * valor_vendido
						custo += custo_item
						lucro = faturamento - custo
			
			faturamento_form = round(faturamento, 2)
			custo_form = round(custo, 2)
			lucro_form = round(lucro, 2)
			
					
			self.faturamento_lucro_mes.append(f'Data: {datas_mes}')
			self.faturamento_lucro_mes.append(f'Faturamento: R${str(faturamento_form)}')
			self.faturamento_lucro_mes.append(f'Lucro: R${str(lucro_form)}')
			self.faturamento_lucro_mes.append('')
			
	def	ano_tedit_set(self):
		self.faturamento_lucro_ano.clear()
		datas_ano = []
		#Adiciona as datas na lista
		for codigo, value in self.historico_vendas.items():
			if value['info']['ano'] not in datas_ano:
				datas_ano.append(self.historico_vendas[codigo]['info']['ano'])
			if value['info']['ano'] in datas_ano:
				pass
		
		for datas in datas_ano:
			faturamento = 0
			custo = 0
			lucro = 0
			for codigo, value in self.historico_vendas.items():
				if value['info']['ano'] == datas:
					for item, info_item in value['itens'].items():
						quantidade = info_item['quantidade']
						valor_vendido = info_item['valor']
						total_item = quantidade * valor_vendido
						faturamento += total_item
					
					for item, info_item in value['itens'].items():
						quantidade = info_item['quantidade']
						valor_vendido = info_item['custo']
						custo_item = quantidade * valor_vendido
						custo += custo_item
						lucro = faturamento - custo
			
			faturamento_form = round(faturamento, 2)
			custo_form = round(custo, 2)
			lucro_form = round(lucro, 2)
			
					
			self.faturamento_lucro_ano.append(f'Ano: {datas}')
			self.faturamento_lucro_ano.append(f'Faturamento: R${str(faturamento_form)}')
			self.faturamento_lucro_ano.append(f'Lucro: R${str(lucro_form)}')
			self.faturamento_lucro_ano.append('')		
			

		
	#Verifica a entrada do self.pesquisa_item_ed para mostrar apenas as
	#vendas que tem esse item		
	def pesquisa_combo_historico_vendas(self):
		itens = []
		self.item_pesquisa_combo.clear()
		item = self.pesquisa_item_ed.text()
		
		
		if self.pesquisa_item_ed.text() == '':
			self.item_pesquisa_combo.clear()
			
		else:
			for item, info in self.estoque.items():
				if self.pesquisa_item_ed.text() in item:
					itens.append(item)
		
			self.item_pesquisa_combo.addItems(itens)	
	
	def cancelar_venda(self):
		if self.codigo_venda_ed.text() in list(self.historico_vendas.keys()):
			self.carregar_historico_vendas()
			for codigo, value in self.historico_vendas.items():
				if codigo == self.codigo_venda_ed.text():
					for item, info_item in value['itens'].items():
						self.estoque[item]['quantidade'] += info_item['quantidade']
						info_item['quantidade'] = 0
			self.salvar_historico_vendas_json()
			self.salvar_estoque()
			self.historico_vendas_tedit_set()
		
		if self.codigo_venda_ed.text() not in list(self.historico_vendas.keys()):
			QMessageBox.warning(self, 'Error ao procurar venda',
			f' Venda de codigo -{self.codigo_venda_ed.text()}- não encontrada!!!',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
			self.codigo_venda_ed.clear()
						
	def quantidade_itens(self):
		quantidade = len(list(self.estoque.keys()))
		self.quantidade_itens_label.setText(f'Quantidade de itens: {quantidade}')
		
	def valor_custo_estoque(self, checked):
		self.custo_total = 0
		
		self.preco_total = 0
		if checked ==  False:
			self.carregar_estoque()
		
			for item, info in self.estoque.items():
				icms = 0.18
				self.custo_total += (self.estoque[item]['custo'] * self.estoque[item]['quantidade'])
				self.preco_total += (self.estoque[item]['valor'] * self.estoque[item]['quantidade'])
			self.custo_total += icms * self.custo_total
			self.valor_estoque.setText(f'Custo: R$ {round(self.custo_total,2)} / Preço: R$ {round(self.preco_total, 2)}')
		
		if checked == True:
			self.valor_estoque.setText(f'Custo: R$ ****** / Preço: R$ ******')
			
			
	def atualizar_preco_sugerido(self):
		
		try:
			dicionario = self.historico_vendas
			vezes_item_vendido = {} #Quantas vendas o item esta presente
			valor_vendido_somado = {} #Somatoria de preco vendido unitario por venda
			item_preco_sugerido_dic = {} #Item vendido e preco sugerido
	
			data = self.data_minima_ed.text()
			try:
				data_formatada = datetime.strptime(data, '%d-%m-%y')
			except:
				data = ''
	
			if data == '':
				#Vezes que o item foi vendido
				for codigo, valor in dicionario.items():
					for item, info in valor['itens'].items():
						if item in vezes_item_vendido:
							vezes_item_vendido[item] += 1			
			
						if item not in vezes_item_vendido:
							vezes_item_vendido[item] = 1
	
				#Preco médio vendido por item
						if item in valor_vendido_somado:
							valor_vendido_somado[item] += info['valor']
				
						if item not in valor_vendido_somado:
							valor_vendido_somado[item] = info['valor']
	
	
	
				#Preco sujerido			
				for item, quantidade in vezes_item_vendido.items():
					item_preco_sugerido_dic[item] = valor_vendido_somado[item] / vezes_item_vendido[item]
	

			if data != '':
				#Vezes que o item foi vendido
				for codigo, valor in dicionario.items():
					data_venda = datetime.strptime(valor['info']['data'], '%d-%m-%y')
		
					for item, info in valor['itens'].items():
						if data_venda >= data_formatada:
							if item in vezes_item_vendido:
								vezes_item_vendido[item] += 1			
			
							if item not in vezes_item_vendido:
								vezes_item_vendido[item] = 1
	
					#Preco médio vendido por item
							if item in valor_vendido_somado:
								valor_vendido_somado[item] += info['valor']
				
							if item not in valor_vendido_somado:
								valor_vendido_somado[item] = info['valor']

				#Preco sujerido			
				for item, quantidade in vezes_item_vendido.items():
					item_preco_sugerido_dic[item] = valor_vendido_somado[item] / vezes_item_vendido[item]
	
			
			self.preco_sugerido_dic = item_preco_sugerido_dic
			self.salvar_preco_sugerido()
		except:
			pass
			
	def adicionar_item(self):
		
		self.window = Adicionar_item_dialog()
		self.window.show()
		
	def adicionar_categoria(self):
		self.window = Adicionar_Categoria()
		self.window.show()
		
	def adicionar_sub_categoria(self):
		self.window = Adicionar_sub_categoria()
		self.window.show()
		
	def remover_item(self):
		self.window = Remover_item_estoque()
		self.window.show()
		
	def editar_item(self):
		self.window = Editar_item_dialog()
		self.window.show()
	
	def ajustar_custo_preco(self):
		self.window = Ajustar_custo_preco()
		self.window.show()
		
	def adicionar_compra(self):
		self.window = Adicionar_compra()
		self.window.show()
		
	def adicionar_fornecedor(self):
		self.window = Adicionar_fornecedor()
		self.window.show()
		
	def remover_fornecedor(self):
		self.window = Remover_fornecedor()
		self.window.show()
	
	def editar_fornecedor(self):
		self.window = Editar_fornecedor()
		self.window.show()
	
	def adicionar_cliente(self):
		self.window = Adicionar_cliente()
		self.window.show()
		
	def editar_cliente(self):
		self.window = Editar_cliente()
		self.window.show()
	
	def remover_cliente(self):
		self.window = Remover_cliente()
		self.window.show()	
		
	def divida(self):
		self.window = Divida()
		self.window.show()
		
	def nova_venda(self):
		self.window = Nova_venda()
		self.window.show()
		
	def devolver_venda(self):
		self.window = Devolver_venda()
		self.window.show()
		
	def t1001(self):
		self.window = T1001()
		self.window.show()
	
	def atualizar_t1001___(self):
		item_t_e_item_media_anual()

			
		
	
		
	def sobre(self):
		self.window = Sobre_()
		self.window.show()
		

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())
