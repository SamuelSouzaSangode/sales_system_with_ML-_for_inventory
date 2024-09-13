import sys, json
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, 
QPushButton, QComboBox, QLabel, QGridLayout, QDialog, QMessageBox, 
QHBoxLayout, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from datetime import datetime
import locale

class Nova_venda(QDialog):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(300, 300)
		self.setWindowTitle('Nova Venda')
		self.estoque = {}
		self.itens_selecionados_venda = {}
		self.total_venda = 0
		self.historico_vendas = {}
		self.preco_sugerido_dic = {}
		self.carregar_preco_sugerido()
		self.carregar_estoque()
		self.setUpMainWindow()
		self.showMaximized()
		
	def setUpMainWindow(self):
		#Estilo de todos os edits
		estilo_edit = '''
		border-radius: 10px; border: 2px solid gray;'''
		
		#Estilo de todos os botões
		estilo_botao = '''
			QPushButton {background-color: #918787; 
			color: black; 
			border-radius: 10px; 
			border: none;}
            
		QPushButton:pressed {background-color: #D42323;}
		'''
		width_qnt = 50
		
		#Barra de pesquisa dos itens
		self.barra_pesquisa_item_ed = QLineEdit()
		self.barra_pesquisa_item_ed.setPlaceholderText('Item ou parte do nome...')
		self.barra_pesquisa_item_ed.setFixedSize(300, 40)

		self.barra_pesquisa_item_ed.setFont(QFont('Arial', 16))
		self.barra_pesquisa_item_ed.setStyleSheet(estilo_edit)
		self.barra_pesquisa_item_ed.setClearButtonEnabled(True)
		self.barra_pesquisa_item_ed.textEdited.connect(self.pesquisa_combo)

		#Todos os itens filtrados para escolha
		self.itens_estoque_combo = QComboBox()
		self.itens_estoque_combo.setFixedSize(300, 40)
		self.itens_estoque_combo.setFont(QFont('Arial', 16))
		self.itens_estoque_combo.setStyleSheet(estilo_edit)
		self.itens_estoque_combo.addItems(list(self.estoque.keys()))
		self.itens_estoque_combo.currentIndexChanged.connect(self.set_info_combo)
		self.itens_estoque_combo.currentIndexChanged.connect(self.set_info_combo_preco_sugerido)
		
		self.estoque_disponivel_label = QLabel()
		self.estoque_disponivel_label.setFont(QFont('Arial', 16))
		
		self.quantidade_d_label = QLabel('Disp: ')
		self.quantidade_d_label.setFont(QFont('Arial', 16))
		
		quantidade_label = QLabel('Qnt: ')
		quantidade_label.setFont(QFont('Arial', 16))
		
		#Quantidade vendida
		self.quantidade_item_ed = QLineEdit('1')
		self.quantidade_item_ed.setMaximumWidth(80)
		self.quantidade_item_ed.setMaximumHeight(40)
		self.quantidade_item_ed.setFont(QFont('Arial', 16))
		self.quantidade_item_ed.setStyleSheet(estilo_edit)
		self.quantidade_item_ed.textEdited.connect(self.apenas_num_pont_quantidade)
		self.quantidade_item_ed.textEdited.connect(self.set_edit_0)
		self.quantidade_item_ed.textEdited.connect(self.total_set)
		
		preco_label = QLabel('Preço: R$')
		preco_label.setFont(QFont('Arial', 16))
		
		self.preco_sugerido_label = QLabel('T1001: R$ N/A')
		self.preco_sugerido_label.setFont(QFont('Arial', 16))
		
		self.preco_sugerido_check = QCheckBox('Mostrar preço sugerido')
		self.preco_sugerido_check.toggled.connect(self.set_info_combo_preco_sugerido)
		
		
		#Valor do itens na hora da venda
		self.valor_item_ed = QLineEdit()
		self.valor_item_ed.setMaximumWidth(80)
		self.valor_item_ed.setMinimumHeight(40)
		self.valor_item_ed.setFont(QFont('Arial', 16))
		self.valor_item_ed.setStyleSheet(estilo_edit)
		self.valor_item_ed.textEdited.connect(self.apenas_num_pont_valor)
		self.valor_item_ed.textEdited.connect(self.set_edit_0)
		self.valor_item_ed.textEdited.connect(self.total_set)
	
		
		self.valor_total_label = QLabel('Total: R$ 120.00')
		self.valor_total_label.setFont(QFont('Arial', 16))
		
		
		self.lancar_botao = QPushButton('Lançar (F10)')
		self.lancar_botao.setFixedSize(130,40)
		self.lancar_botao.setDefault(True)
		self.lancar_botao.setFont(QFont('Arial', 16))
		self.lancar_botao.setStyleSheet(estilo_botao)
		self.lancar_botao.clicked.connect(self.dicionario_venda_lancar)
		self.lancar_botao.clicked.connect(self.botao_lancar)
		self.lancar_botao.clicked.connect(self.botao_click_barra)
		#Atalho para o lancar_botao = f10
		atalho_lancar_botao = QShortcut(QKeySequence(Qt.Key.Key_F10), self)
		atalho_lancar_botao.activated.connect(self.lancar_botao.click)
		
		self.total_da_venda_label = QLabel('Total: R$ 0')
		self.total_da_venda_label.setFont(QFont('Arial', 16))
		self.total_da_venda_label.setAlignment(Qt.AlignmentFlag.AlignRight)

		total_v_label = QLabel('Total final')
		total_v_label.setFont(QFont('Arial', 16))

		self.total_da_venda_edit = QLineEdit('0')
		self.total_da_venda_edit.setMaximumWidth(60)
		self.total_da_venda_edit.setFont(QFont('Arial', 16))
		self.total_da_venda_edit.textEdited.connect(self.total_da_venda_entrada)

		
		self.botao_finalizar_venda = QPushButton('Finalizar venda (F2)')
		self.botao_finalizar_venda.setStyleSheet(estilo_botao)
		self.botao_finalizar_venda.setMinimumHeight(40)
		self.botao_finalizar_venda.setMinimumWidth(300)
		self.botao_finalizar_venda.setFont(QFont('arial', 16))
		#Atalho para bota_finalizar_venda = F12
		atalho_lancar_botao = QShortcut(QKeySequence(Qt.Key.Key_F2), self)
		atalho_lancar_botao.activated.connect(self.botao_finalizar_venda.click)
		self.botao_finalizar_venda.clicked.connect(self.salvar_itens_selecionados_venda_json)
		
		
		main_h_box_total = QHBoxLayout()
		main_h_box_total.addWidget(total_v_label)
		main_h_box_total.addWidget(self.total_da_venda_edit)
		main_h_box_total.addWidget(self.total_da_venda_label)
		
		
####Itens selcionados para venda #######################################		
		item_label = QLabel('Itens')
		item_label.setFont(QFont('Arial', 16))
		
		unid_label = QLabel('Unid')
		unid_label.setFont(QFont('Arial', 16))
		
		valor_unid = QLabel('Preço ')
		valor_unid.setFont(QFont('Arial', 16))
		
		total_label= QLabel('Total')
		total_label.setFont(QFont('Arial', 16))
		
		'''Item 1'''			
		self.item_label_1 = QLabel()
		self.item_label_1.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_1 = QLineEdit()
		self.unidade_selec_ed_1.setMaximumWidth(60)
		self.unidade_selec_ed_1.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_1.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_1.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_1.textEdited.connect(self.atualizar_quantidade_item_1)
		
		self.valor_selec_ed_1 = QLineEdit()
		self.valor_selec_ed_1.setMaximumWidth(80)
		self.valor_selec_ed_1.setFont(QFont('Arial', 12))
		self.valor_selec_ed_1.setStyleSheet(estilo_edit)
		self.valor_selec_ed_1.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_1.textEdited.connect(self.atualizar_valor_item_1)
										  					
		self.total_item_label_1 = QLabel()
		self.total_item_label_1.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_1 = QPushButton('x')
		self.excluir_item_botao_1.setMaximumWidth(40)
		self.excluir_item_botao_1.clicked.connect(self.botao_deletar_item_1)

		'''Item 2'''
		self.item_label_2 = QLabel()
		self.item_label_2.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_2 = QLineEdit()
		self.unidade_selec_ed_2.setMaximumWidth(60)
		self.unidade_selec_ed_2.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_2.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_2.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_2.textEdited.connect(self.atualizar_quantidade_item_2)
		
		self.valor_selec_ed_2 = QLineEdit()
		self.valor_selec_ed_2.setMaximumWidth(80)
		self.valor_selec_ed_2.setFont(QFont('Arial', 12))
		self.valor_selec_ed_2.setStyleSheet(estilo_edit)
		self.valor_selec_ed_2.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_2.textEdited.connect(self.atualizar_valor_item_2)
		
		self.total_item_label_2 = QLabel()
		self.total_item_label_2.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_2 = QPushButton('x')
		self.excluir_item_botao_2.setMaximumWidth(40)			
		self.excluir_item_botao_2.clicked.connect(self.botao_deletar_item_2)	
		
		'''Item 3'''
		self.item_label_3 = QLabel()
		self.item_label_3.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_3 = QLineEdit()
		self.unidade_selec_ed_3.setMaximumWidth(60)
		self.unidade_selec_ed_3.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_3.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_3.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_3.textEdited.connect(self.atualizar_quantidade_item_3)
		
		self.valor_selec_ed_3 = QLineEdit()
		self.valor_selec_ed_3.setMaximumWidth(80)
		self.valor_selec_ed_3.setFont(QFont('Arial', 12))
		self.valor_selec_ed_3.setStyleSheet(estilo_edit)
		self.valor_selec_ed_3.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_3.textEdited.connect(self.atualizar_valor_item_3)
		
		self.total_item_label_3 = QLabel()
		self.total_item_label_3.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_3 = QPushButton('x')
		self.excluir_item_botao_3.setMaximumWidth(40)	
		self.excluir_item_botao_3.clicked.connect(self.botao_deletar_item_3)	
		
		'''Item 4'''
		self.item_label_4 = QLabel()
		self.item_label_4.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_4 = QLineEdit()
		self.unidade_selec_ed_4.setMaximumWidth(60)
		self.unidade_selec_ed_4.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_4.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_4.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_4.textEdited.connect(self.atualizar_quantidade_item_4)
		
		self.valor_selec_ed_4 = QLineEdit()
		self.valor_selec_ed_4.setMaximumWidth(80)
		self.valor_selec_ed_4.setFont(QFont('Arial', 12))
		self.valor_selec_ed_4.setStyleSheet(estilo_edit)
		self.valor_selec_ed_4.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_4.textEdited.connect(self.atualizar_valor_item_4)
		
		self.total_item_label_4 = QLabel()
		self.total_item_label_4.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_4 = QPushButton('x')
		self.excluir_item_botao_4.setMaximumWidth(40)
		self.excluir_item_botao_4.clicked.connect(self.botao_deletar_item_4)
		
		'''Item 5'''
		self.item_label_5 = QLabel()
		self.item_label_5.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_5 = QLineEdit()
		self.unidade_selec_ed_5.setMaximumWidth(60)
		self.unidade_selec_ed_5.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_5.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_5.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_5.textEdited.connect(self.atualizar_quantidade_item_5)
		
		self.valor_selec_ed_5 = QLineEdit()
		self.valor_selec_ed_5.setMaximumWidth(80)
		self.valor_selec_ed_5.setFont(QFont('Arial', 12))
		self.valor_selec_ed_5.setStyleSheet(estilo_edit)
		self.valor_selec_ed_5.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_5.textEdited.connect(self.atualizar_valor_item_5)
		
		self.total_item_label_5 = QLabel()
		self.total_item_label_5.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_5 = QPushButton('x')
		self.excluir_item_botao_5.setMaximumWidth(40)		
		self.excluir_item_botao_5.clicked.connect(self.botao_deletar_item_5)
		
		'''Item 6'''
		self.item_label_6 = QLabel()
		self.item_label_6.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_6 = QLineEdit()
		self.unidade_selec_ed_6.setMaximumWidth(60)
		self.unidade_selec_ed_6.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_6.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_6.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_6.textEdited.connect(self.atualizar_quantidade_item_6)
		
		self.valor_selec_ed_6 = QLineEdit()
		self.valor_selec_ed_6.setMaximumWidth(80)
		self.valor_selec_ed_6.setFont(QFont('Arial', 12))
		self.valor_selec_ed_6.setStyleSheet(estilo_edit)
		self.valor_selec_ed_6.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_6.textEdited.connect(self.atualizar_valor_item_6)
		
		self.total_item_label_6 = QLabel()
		self.total_item_label_6.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_6 = QPushButton('x')
		self.excluir_item_botao_6.setMaximumWidth(40)		
		self.excluir_item_botao_6.clicked.connect(self.botao_deletar_item_6)
		
		'''Item 7'''
		self.item_label_7 = QLabel()
		self.item_label_7.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_7 = QLineEdit()
		self.unidade_selec_ed_7.setMaximumWidth(60)
		self.unidade_selec_ed_7.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_7.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_7.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_7.textEdited.connect(self.atualizar_quantidade_item_7)
		
		self.valor_selec_ed_7 = QLineEdit()
		self.valor_selec_ed_7.setMaximumWidth(80)
		self.valor_selec_ed_7.setFont(QFont('Arial', 12))
		self.valor_selec_ed_7.setStyleSheet(estilo_edit)
		self.valor_selec_ed_7.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_7.textEdited.connect(self.atualizar_valor_item_7)
		
		self.total_item_label_7 = QLabel()
		self.total_item_label_7.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_7 = QPushButton('x')
		self.excluir_item_botao_7.setMaximumWidth(40)
		self.excluir_item_botao_7.clicked.connect(self.botao_deletar_item_7)
		
		'''Item 8'''
		self.item_label_8 = QLabel()
		self.item_label_8.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_8 = QLineEdit()
		self.unidade_selec_ed_8.setMaximumWidth(60)
		self.unidade_selec_ed_8.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_8.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_8.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_8.textEdited.connect(self.atualizar_quantidade_item_8)
		
		self.valor_selec_ed_8 = QLineEdit()
		self.valor_selec_ed_8.setMaximumWidth(80)
		self.valor_selec_ed_8.setFont(QFont('Arial', 12))
		self.valor_selec_ed_8.setStyleSheet(estilo_edit)
		self.valor_selec_ed_8.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_8.textEdited.connect(self.atualizar_valor_item_8)
		
		self.total_item_label_8 = QLabel()
		self.total_item_label_8.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_8 = QPushButton('x')
		self.excluir_item_botao_8.setMaximumWidth(40)		
		self.excluir_item_botao_8.clicked.connect(self.botao_deletar_item_8)
		
		'''Item 9'''
		self.item_label_9 = QLabel()
		self.item_label_9.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_9 = QLineEdit()
		self.unidade_selec_ed_9.setMaximumWidth(60)
		self.unidade_selec_ed_9.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_9.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_9.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_9.textEdited.connect(self.atualizar_quantidade_item_9)
		
		self.valor_selec_ed_9 = QLineEdit()
		self.valor_selec_ed_9.setMaximumWidth(80)
		self.valor_selec_ed_9.setFont(QFont('Arial', 12))
		self.valor_selec_ed_9.setStyleSheet(estilo_edit)
		self.valor_selec_ed_9.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_9.textEdited.connect(self.atualizar_valor_item_9)
		
		self.total_item_label_9 = QLabel()
		self.total_item_label_9.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_9 = QPushButton('x')
		self.excluir_item_botao_9.setMaximumWidth(40)		
		self.excluir_item_botao_9.clicked.connect(self.botao_deletar_item_9)		
		
		'''Item 10'''
		self.item_label_10 = QLabel()
		self.item_label_10.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_10 = QLineEdit()
		self.unidade_selec_ed_10.setMaximumWidth(60)
		self.unidade_selec_ed_10.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_10.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_10.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_10.textEdited.connect(self.atualizar_quantidade_item_10)
		
		self.valor_selec_ed_10 = QLineEdit()
		self.valor_selec_ed_10.setMaximumWidth(80)
		self.valor_selec_ed_10.setFont(QFont('Arial', 12))
		self.valor_selec_ed_10.setStyleSheet(estilo_edit)
		self.valor_selec_ed_10.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_10.textEdited.connect(self.atualizar_valor_item_10)
		
		self.total_item_label_10 = QLabel()
		self.total_item_label_10.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_10 = QPushButton('x')
		self.excluir_item_botao_10.setMaximumWidth(40)				
		self.excluir_item_botao_10.clicked.connect(self.botao_deletar_item_10)
		
		'''Item 11'''
		self.item_label_11 = QLabel()
		self.item_label_11.setFont(QFont('Arial', 12))
	
		self.unidade_selec_ed_11 = QLineEdit()
		self.unidade_selec_ed_11.setMaximumWidth(60)
		self.unidade_selec_ed_11.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_11.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_11.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_11.textEdited.connect(self.atualizar_quantidade_item_11)
		
		self.valor_selec_ed_11 = QLineEdit()
		self.valor_selec_ed_11.setMaximumWidth(80)
		self.valor_selec_ed_11.setFont(QFont('Arial', 12))
		self.valor_selec_ed_11.setStyleSheet(estilo_edit)
		self.valor_selec_ed_11.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_11.textEdited.connect(self.atualizar_valor_item_11)
		
		self.total_item_label_11 = QLabel()
		self.total_item_label_11.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_11 = QPushButton('x')
		self.excluir_item_botao_11.setMaximumWidth(40)
		self.excluir_item_botao_11.clicked.connect(self.botao_deletar_item_11)
		
		'''Item 12'''
		self.item_label_12 = QLabel()
		self.item_label_12.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_12 = QLineEdit()
		self.unidade_selec_ed_12.setMaximumWidth(60)
		self.unidade_selec_ed_12.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_12.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_12.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_12.textEdited.connect(self.atualizar_quantidade_item_12)
		
		self.valor_selec_ed_12 = QLineEdit()
		self.valor_selec_ed_12.setMaximumWidth(80)
		self.valor_selec_ed_12.setFont(QFont('Arial', 12))
		self.valor_selec_ed_12.setStyleSheet(estilo_edit)
		self.valor_selec_ed_12.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_12.textEdited.connect(self.atualizar_valor_item_12)
		
		self.total_item_label_12 = QLabel()
		self.total_item_label_12.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_12 = QPushButton('x')
		self.excluir_item_botao_12.setMaximumWidth(40)
		self.excluir_item_botao_12.clicked.connect(self.botao_deletar_item_12)			
			
		'''Item 13'''
		self.item_label_13 = QLabel()
		self.item_label_13.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_13 = QLineEdit()
		self.unidade_selec_ed_13.setMaximumWidth(60)
		self.unidade_selec_ed_13.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_13.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_13.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_13.textEdited.connect(self.atualizar_quantidade_item_13)
		
		self.valor_selec_ed_13 = QLineEdit()
		self.valor_selec_ed_13.setMaximumWidth(80)
		self.valor_selec_ed_13.setFont(QFont('Arial', 12))
		self.valor_selec_ed_13.setStyleSheet(estilo_edit)
		self.valor_selec_ed_13.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_13.textEdited.connect(self.atualizar_valor_item_13)
		
		self.total_item_label_13 = QLabel()
		self.total_item_label_13.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_13 = QPushButton('x')
		self.excluir_item_botao_13.setMaximumWidth(40)	
		self.excluir_item_botao_13.clicked.connect(self.botao_deletar_item_13)
			
		'''Item 14'''
		self.item_label_14 = QLabel()
		self.item_label_14.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_14 = QLineEdit()
		self.unidade_selec_ed_14.setMaximumWidth(60)
		self.unidade_selec_ed_14.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_14.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_14.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_14.textEdited.connect(self.atualizar_quantidade_item_14)
		
		self.valor_selec_ed_14 = QLineEdit()
		self.valor_selec_ed_14.setMaximumWidth(80)
		self.valor_selec_ed_14.setFont(QFont('Arial', 12))
		self.valor_selec_ed_14.setStyleSheet(estilo_edit)
		self.valor_selec_ed_14.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_14.textEdited.connect(self.atualizar_valor_item_14)
		
		self.total_item_label_14 = QLabel()
		self.total_item_label_14.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_14 = QPushButton('x')
		self.excluir_item_botao_14.setMaximumWidth(40)
		self.excluir_item_botao_14.clicked.connect(self.botao_deletar_item_14
		)
		'''Item 15'''
		self.item_label_15 = QLabel()
		self.item_label_15.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_15 = QLineEdit()
		self.unidade_selec_ed_15.setMaximumWidth(60)
		self.unidade_selec_ed_15.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_15.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_15.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_15.textEdited.connect(self.atualizar_quantidade_item_15)
		
		self.valor_selec_ed_15 = QLineEdit()
		self.valor_selec_ed_15.setMaximumWidth(80)
		self.valor_selec_ed_15.setFont(QFont('Arial', 12))
		self.valor_selec_ed_15.setStyleSheet(estilo_edit)
		self.valor_selec_ed_15.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_15.textEdited.connect(self.atualizar_valor_item_15)
		
		self.total_item_label_15 = QLabel()
		self.total_item_label_15.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_15 = QPushButton('x')
		self.excluir_item_botao_15.setMaximumWidth(40)
		self.excluir_item_botao_15.clicked.connect(self.botao_deletar_item_15)		
		
		'''Item 16'''
		self.item_label_16 = QLabel()
		self.item_label_16.setFont(QFont('Arial', 12))
		
		self.unidade_selec_ed_16 = QLineEdit()
		self.unidade_selec_ed_16.setMaximumWidth(60)
		self.unidade_selec_ed_16.setFont(QFont('Arial', 12))
		self.unidade_selec_ed_16.setStyleSheet(estilo_edit)
		self.unidade_selec_ed_16.textEdited.connect(self.apenas_num_pont)
		self.unidade_selec_ed_16.textEdited.connect(self.atualizar_quantidade_item_16)
		
		self.valor_selec_ed_16 = QLineEdit()
		self.valor_selec_ed_16.setMaximumWidth(80)
		self.valor_selec_ed_16.setFont(QFont('Arial', 12))
		self.valor_selec_ed_16.setStyleSheet(estilo_edit)
		self.valor_selec_ed_16.textEdited.connect(self.apenas_num_pont)
		self.valor_selec_ed_16.textEdited.connect(self.atualizar_valor_item_16)
		
		self.total_item_label_16 = QLabel()
		self.total_item_label_16.setFont(QFont('Arial', 12))
		
		self.excluir_item_botao_16 = QPushButton('x')
		self.excluir_item_botao_16.setMaximumWidth(40)
		self.excluir_item_botao_16.clicked.connect(self.botao_deletar_item_16)		

				

		main_grid_venda = QGridLayout()
		main_grid_venda.addWidget(self.barra_pesquisa_item_ed, 0, 0)
		main_grid_venda.addWidget(self.itens_estoque_combo, 1, 0)
		main_grid_venda.addWidget(self.quantidade_d_label, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
		#main_grid_venda.addWidget(self.estoque_disponivel_label, 1, 2)
		main_grid_venda.addWidget(quantidade_label, 1, 3, 1, 2)
		main_grid_venda.addWidget(self.quantidade_item_ed, 1, 4, alignment=Qt.AlignmentFlag.AlignLeft)
		main_grid_venda.addWidget(self.preco_sugerido_label, 0, 6, alignment=Qt.AlignmentFlag.AlignLeft)
		main_grid_venda.addWidget(self.preco_sugerido_check, 0, 4, alignment=Qt.AlignmentFlag.AlignLeft)
		main_grid_venda.addWidget(preco_label, 1, 6)
		main_grid_venda.addWidget(self.valor_item_ed, 1, 7)
		main_grid_venda.addWidget(self.valor_total_label, 1, 8)
		main_grid_venda.addWidget(self.lancar_botao, 1, 9)
		main_grid_venda.addWidget(item_label, 2, 0)
		main_grid_venda.addWidget(unid_label, 2, 3)
		main_grid_venda.addWidget(valor_unid, 2, 6)
		main_grid_venda.addWidget(total_label, 2, 9)
		main_grid_venda.addWidget(self.item_label_1, 3, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_1, 3, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_1, 3, 6)
		main_grid_venda.addWidget(self.total_item_label_1, 3, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_1, 3, 9, alignment=Qt.AlignmentFlag.AlignRight)
		main_grid_venda.addWidget(self.item_label_2, 4, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_2, 4, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_2, 4, 6)
		main_grid_venda.addWidget(self.total_item_label_2, 4, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_2, 4, 9, alignment=Qt.AlignmentFlag.AlignRight)
		main_grid_venda.addWidget(self.item_label_3, 5, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_3, 5, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_3, 5, 6)
		main_grid_venda.addWidget(self.total_item_label_3, 5, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_3, 5, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_4, 6, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_4, 6, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_4, 6, 6)
		main_grid_venda.addWidget(self.total_item_label_4, 6, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_4, 6, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_5, 7, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_5, 7, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_5, 7, 6)
		main_grid_venda.addWidget(self.total_item_label_5, 7, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_5, 7, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_6, 8, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_6, 8, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_6, 8, 6)
		main_grid_venda.addWidget(self.total_item_label_6, 8, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_6, 8, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_7, 9, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_7, 9, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_7, 9, 6)
		main_grid_venda.addWidget(self.total_item_label_7, 9, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_7, 9, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_8, 10, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_8, 10, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_8, 10, 6)
		main_grid_venda.addWidget(self.total_item_label_8, 10, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_8, 10, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_9, 11, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_9, 11, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_9, 11, 6)
		main_grid_venda.addWidget(self.total_item_label_9, 11, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_9, 11, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_10, 12, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_10, 12, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_10, 12, 6)
		main_grid_venda.addWidget(self.total_item_label_10, 12, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_10, 12, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_11, 13, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_11, 13, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_11, 13, 6)
		main_grid_venda.addWidget(self.total_item_label_11, 13, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_11, 13, 9, alignment=Qt.AlignmentFlag.AlignRight)
		main_grid_venda.addWidget(self.item_label_12, 14, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_12, 14, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_12, 14, 6)
		main_grid_venda.addWidget(self.total_item_label_12, 14, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_12, 14, 9, alignment=Qt.AlignmentFlag.AlignRight)
		main_grid_venda.addWidget(self.item_label_13, 15, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_13, 15, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_13, 15, 6)
		main_grid_venda.addWidget(self.total_item_label_13, 15, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_13, 15, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_14, 16, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_14, 16, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_14, 16, 6)
		main_grid_venda.addWidget(self.total_item_label_14, 16, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_14, 16, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_15, 17, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_15, 17, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_15, 17, 6)
		main_grid_venda.addWidget(self.total_item_label_15, 17, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_15, 17, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addWidget(self.item_label_16, 18, 0)
		main_grid_venda.addWidget(self.unidade_selec_ed_16, 18, 3)
		main_grid_venda.addWidget(self.valor_selec_ed_16, 18, 6)
		main_grid_venda.addWidget(self.total_item_label_16, 18, 9)
		main_grid_venda.addWidget(self.excluir_item_botao_16, 18, 9, alignment=Qt.AlignmentFlag.AlignRight)		
		main_grid_venda.addLayout(main_h_box_total, 19, 8, 1, 2)
		main_grid_venda.addWidget(self.botao_finalizar_venda, 20, 8, 1, 2)
		









		
		
		main_grid_venda.setAlignment(Qt.AlignmentFlag.AlignTop)
		
		
		self.setLayout(main_grid_venda)
		self.set_info_combo()
	
	#Coloca as informações do item no cabeçalho de venda	
	def set_info_combo(self):
		item = self.itens_estoque_combo.currentText()
		self.quantidade_item_ed.setText('1')
		
		if item != '':
			valor_unitario = (self.estoque[item]['valor'])
			total = (float(self.quantidade_item_ed.text()) * valor_unitario)
			total_form = round(total, 2)
			
			self.valor_item_ed.setText(str(valor_unitario))
			self.quantidade_d_label.setText(f"Disp: {str(self.estoque[item]['quantidade'])}")
			self.valor_total_label.setText(f' Total: R$ {str(total_form)}')
		else:
			pass
			
	def set_info_combo_preco_sugerido(self, checked):
		item = self.itens_estoque_combo.currentText()
		preco_sugerido_formatado = 0

		if item != '':
			if item in self.preco_sugerido_dic:
				if self.preco_sugerido_check.isChecked():
					preco_sugerido = self.preco_sugerido_dic[item]
					preco_sugerido_corrigido = preco_sugerido + (preco_sugerido * 0.03)
					preco_sugerido_formatado = round(preco_sugerido_corrigido, 2)
					self.preco_sugerido_label.setText(f'T1001: R$ {preco_sugerido_formatado}')			
				else: 
					self.preco_sugerido_label.setText('T1001: R$ N/A')
			if item not in self.preco_sugerido_dic:
				self.preco_sugerido_label.setText('T1001: R$ N/A')
			
		else:
			self.preco_sugerido_label.setText('T1001: R$ N/A')
		
	
	#Coloca os itens no combobox	
	def pesquisa_combo(self):
		itens = []
		self.itens_estoque_combo.clear()
		item = self.itens_estoque_combo.currentText()
		
		
		if self.barra_pesquisa_item_ed.text() == '':
			self.itens_estoque_combo.addItems(list(self.estoque.keys()))
			
		else:
			for item, info in self.estoque.items():
				if self.barra_pesquisa_item_ed.text() in item:
					itens.append(item)
		
			self.itens_estoque_combo.addItems(itens)		
	
	#Não deixa o lineedit fica sem nada	
	def set_edit_0(self):
		if self.quantidade_item_ed.text() == '':
			self.quantidade_item_ed.setText('0')
			
		if self.valor_item_ed.text() == '':
			self.valor_item_ed.setText('0')
	
	#Mostra o total no cabeçalho
	def total_set(self):
		quantidade = self.quantidade_item_ed.text()
		valor_unitario = self.valor_item_ed.text()
		total = (float(quantidade) * float(valor_unitario))
		total_form = round(total, 2)
		self.valor_total_label.setText(f' Total: R$ {str(total_form)}')
	
	#Gera o proximo código de venda
	def gerar_proximo_codigo_venda(self):
		
		if not self.historico_vendas:
			return 1
		maior_numero_venda = max(map(int, self.historico_vendas.keys()))
		novo_numero_venda = maior_numero_venda + 1
		return novo_numero_venda	
	
	#Dicionário com os itens selecionados para venda		
	def dicionario_venda_lancar(self):
		if self.itens_estoque_combo.currentText() == '':
			QMessageBox.warning(self, 'Item não encontrado',
			'Atenção o item deve ter sido selecionado!!!!!',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
		
		else:
			'''Toda vez que o botão LANÇAR for clicado irá ascresentar 
			item na lista e suas informaçoes.
			Na ultima parte ele somará o total de cada item e somará ao
			toal da venda, isso será feito toda vez'''
			
		
			info = {}
			item = self.itens_estoque_combo.currentText()
			quantidade = float(self.quantidade_item_ed.text())
			valor = float(self.valor_item_ed.text())
		
			info['quantidade'] = quantidade
			info['valor'] = valor
			info['custo'] = self.estoque[item]['custo']
		
			self.itens_selecionados_venda[item] = info
			print(self.itens_selecionados_venda)
			
	#Pega os itens do dicionário e coloca na parte de vendas	
	def botao_lancar(self):

		#Mostra o total de venda de todos os itens
		total_da_venda = 0	
		for item, info in self.itens_selecionados_venda.items():
			total_da_venda += info['quantidade'] * info['valor']
			total_da_venda_form = round(total_da_venda, 2)	
		try:
			self.total_da_venda_label.setText(str(f' Total: R$ {total_da_venda_form}'))
		except UnboundLocalError:
			self.total_da_venda_label.setText(str(' Total: R$ 0'))
		
		
		'''Essa parte mostra para o usuário'''
		
		lista_de_itens = list(self.itens_selecionados_venda.keys())
		if len(lista_de_itens) <= 15:
			self.lancar_botao.setEnabled(True)
		else:
			self.lancar_botao.setEnabled(False)
		
		#Limpa todos labels e edits depois do cabeçalho
		self.item_label_1.setText('')
		self.unidade_selec_ed_1.clear()
		self.valor_selec_ed_1.clear()
		self.total_item_label_1.setText('')
		
		self.item_label_2.setText('')
		self.unidade_selec_ed_2.clear()
		self.valor_selec_ed_2.clear()
		self.total_item_label_2.setText('')	
		
		self.item_label_3.setText('')
		self.unidade_selec_ed_3.clear()
		self.valor_selec_ed_3.clear()
		self.total_item_label_3.setText('')	
		
		self.item_label_4.setText('')
		self.unidade_selec_ed_4.clear()
		self.valor_selec_ed_4.clear()
		self.total_item_label_4.setText('')
		
		self.item_label_5.setText('')
		self.unidade_selec_ed_5.clear()
		self.valor_selec_ed_5.clear()
		self.total_item_label_5.setText('')		
			
		self.item_label_6.setText('')
		self.unidade_selec_ed_6.clear()
		self.valor_selec_ed_6.clear()
		self.total_item_label_6.setText('')		
		
		self.item_label_7.setText('')
		self.unidade_selec_ed_7.clear()
		self.valor_selec_ed_7.clear()
		self.total_item_label_7.setText('')		
		
		self.item_label_8.setText('')
		self.unidade_selec_ed_8.clear()
		self.valor_selec_ed_8.clear()
		self.total_item_label_8.setText('')		
		
		self.item_label_9.setText('')
		self.unidade_selec_ed_9.clear()
		self.valor_selec_ed_9.clear()
		self.total_item_label_9.setText('')
		
		self.item_label_10.setText('')
		self.unidade_selec_ed_10.clear()
		self.valor_selec_ed_10.clear()
		self.total_item_label_10.setText('')		
		
		self.item_label_11.setText('')
		self.unidade_selec_ed_11.clear()
		self.valor_selec_ed_11.clear()
		self.total_item_label_11.setText('')		
			
		self.item_label_12.setText('')
		self.unidade_selec_ed_12.clear()
		self.valor_selec_ed_12.clear()
		self.total_item_label_12.setText('')		
		
		self.item_label_13.setText('')
		self.unidade_selec_ed_13.clear()
		self.valor_selec_ed_13.clear()
		self.total_item_label_13.setText('')	
		
		self.item_label_14.setText('')
		self.unidade_selec_ed_14.clear()
		self.valor_selec_ed_14.clear()
		self.total_item_label_14.setText('')		
		
		self.item_label_15.setText('')
		self.unidade_selec_ed_15.clear()
		self.valor_selec_ed_15.clear()
		self.total_item_label_15.setText('')		
		
		self.item_label_16.setText('')
		self.unidade_selec_ed_16.clear()
		self.valor_selec_ed_16.clear()
		self.total_item_label_16.setText('')		
	
		try:
			item_1 = lista_de_itens[0]
			quantidade_1 = str(self.itens_selecionados_venda[item_1]['quantidade'])
			valor_1 = str(self.itens_selecionados_venda[item_1]['valor'])
			total_1 = (float(quantidade_1) * float(valor_1))
			total_1_form = str(round(total_1, 2))
			
			
			self.item_label_1.setText(item_1)
			self.unidade_selec_ed_1.setText(quantidade_1)
			self.valor_selec_ed_1.setText(valor_1)
			self.total_item_label_1.setText(total_1_form)
		except:
				pass			
			
		try:	
			item_2 = lista_de_itens[1]
			quantidade_2 = str(self.itens_selecionados_venda[item_2]['quantidade'])
			valor_2 = str(self.itens_selecionados_venda[item_2]['valor'])
			total_2 = (float(quantidade_2) * float(valor_2))
			total_2_form = str(round(total_2, 2))

			
			self.item_label_2.setText(item_2)
			self.unidade_selec_ed_2.setText(quantidade_2)
			self.valor_selec_ed_2.setText(valor_2)
			self.total_item_label_2.setText(total_2_form)
		except:
			pass
			
		try:	
			item_3 = lista_de_itens[2]
			quantidade_3 = str(self.itens_selecionados_venda[item_3]['quantidade'])
			valor_3 = str(self.itens_selecionados_venda[item_3]['valor'])
			total_3 = (float(quantidade_3) * float(valor_3))
			total_3_form = str(round(total_3, 2))
			
			self.item_label_3.setText(item_3)
			self.unidade_selec_ed_3.setText(quantidade_3)
			self.valor_selec_ed_3.setText(valor_3)
			self.total_item_label_3.setText(total_3_form)
		except:
			pass			
			
		try:	
			item_4 = lista_de_itens[3]
			quantidade_4 = str(self.itens_selecionados_venda[item_4]['quantidade'])
			valor_4 = str(self.itens_selecionados_venda[item_4]['valor'])
			total_4 = (float(quantidade_4) * float(valor_4))
			total_4_form = str(round(total_4, 2))
			
			self.item_label_4.setText(item_4)
			self.unidade_selec_ed_4.setText(quantidade_4)
			self.valor_selec_ed_4.setText(valor_4)
			self.total_item_label_4.setText(total_4_form)
		except:
			pass			
			
		try:	
			item_5 = lista_de_itens[4]
			quantidade_5 = str(self.itens_selecionados_venda[item_5]['quantidade'])
			valor_5 = str(self.itens_selecionados_venda[item_5]['valor'])
			total_5 = (float(quantidade_5) * float(valor_5))
			total_5_form = str(round(total_5, 2))
			
			self.item_label_5.setText(item_5)
			self.unidade_selec_ed_5.setText(quantidade_5)
			self.valor_selec_ed_5.setText(valor_5)
			self.total_item_label_5.setText(total_5_form)
		except:
			pass			
			
		try:	
			item_6 = lista_de_itens[5]
			quantidade_6 = str(self.itens_selecionados_venda[item_6]['quantidade'])
			valor_6 = str(self.itens_selecionados_venda[item_6]['valor'])
			total_6 = (float(quantidade_6) * float(valor_6))
			total_6_form = str(round(total_6, 2))
			
			self.item_label_6.setText(item_6)
			self.unidade_selec_ed_6.setText(quantidade_6)
			self.valor_selec_ed_6.setText(valor_6)
			self.total_item_label_6.setText(total_6_form)
		except:
			pass			
			
		try:	
			item_7 = lista_de_itens[6]
			quantidade_7 = str(self.itens_selecionados_venda[item_7]['quantidade'])
			valor_7 = str(self.itens_selecionados_venda[item_7]['valor'])
			total_7 = (float(quantidade_7) * float(valor_7))
			total_7_form = str(round(total_7, 2))
			self.total_venda += total_7
			
			self.item_label_7.setText(item_7)
			self.unidade_selec_ed_7.setText(quantidade_7)
			self.valor_selec_ed_7.setText(valor_7)
			self.total_item_label_7.setText(total_7_form)
		except:
			pass			

		try:	
			item_8 = lista_de_itens[7]
			quantidade_8 = str(self.itens_selecionados_venda[item_8]['quantidade'])
			valor_8 = str(self.itens_selecionados_venda[item_8]['valor'])
			total_8 = (float(quantidade_7) * float(valor_8))
			total_8_form = str(round(total_8, 2))

			
			self.item_label_8.setText(item_8)
			self.unidade_selec_ed_8.setText(quantidade_8)
			self.valor_selec_ed_8.setText(valor_8)
			self.total_item_label_8.setText(total_8_form)
		except:
			pass			

		try:	
			item_9 = lista_de_itens[8]
			quantidade_9 = str(self.itens_selecionados_venda[item_9]['quantidade'])
			valor_9 = str(self.itens_selecionados_venda[item_9]['valor'])
			total_9 = (float(quantidade_9) * float(valor_9))
			total_9_form = str(round(total_9, 2))
			
			self.item_label_9.setText(item_9)
			self.unidade_selec_ed_9.setText(quantidade_9)
			self.valor_selec_ed_9.setText(valor_9)
			self.total_item_label_9.setText(total_9_form)
		except:
			pass

		try:	
			item_10 = lista_de_itens[9]
			quantidade_10 = str(self.itens_selecionados_venda[item_10]['quantidade'])
			valor_10 = str(self.itens_selecionados_venda[item_10]['valor'])
			total_10 = (float(quantidade_10) * float(valor_10))
			total_10_form = str(round(total_10, 2))
			
			self.item_label_10.setText(item_10)
			self.unidade_selec_ed_10.setText(quantidade_10)
			self.valor_selec_ed_10.setText(valor_10)
			self.total_item_label_10.setText(total_10_form)
		except:
			pass

		try:	
			item_11 = lista_de_itens[10]
			quantidade_11 = str(self.itens_selecionados_venda[item_11]['quantidade'])
			valor_11 = str(self.itens_selecionados_venda[item_11]['valor'])
			total_11 = (float(quantidade_11) * float(valor_11))
			total_11_form = str(round(total_11, 2))
			
			self.item_label_11.setText(item_11)
			self.unidade_selec_ed_11.setText(quantidade_11)
			self.valor_selec_ed_11.setText(valor_11)
			self.total_item_label_11.setText(total_11_form)
		except:
			pass

		try:	
			item_12 = lista_de_itens[11]
			quantidade_12 = str(self.itens_selecionados_venda[item_12]['quantidade'])
			valor_12 = str(self.itens_selecionados_venda[item_12]['valor'])
			total_12 = (float(quantidade_12) * float(valor_12))
			total_12_form = str(round(total_12, 2))
			
			self.item_label_12.setText(item_12)
			self.unidade_selec_ed_12.setText(quantidade_12)
			self.valor_selec_ed_12.setText(valor_12)
			self.total_item_label_12.setText(total_12_form)
		except:
			pass

		try:	
			item_13 = lista_de_itens[12]
			quantidade_13 = str(self.itens_selecionados_venda[item_13]['quantidade'])
			valor_13 = str(self.itens_selecionados_venda[item_13]['valor'])
			total_13 = (float(quantidade_13) * float(valor_13))
			total_13_form = str(round(total_13, 2))
			
			self.item_label_13.setText(item_13)
			self.unidade_selec_ed_13.setText(quantidade_13)
			self.valor_selec_ed_13.setText(valor_13)
			self.total_item_label_13.setText(total_3_form)
		except:
			pass

		try:	
			item_14 = lista_de_itens[13]
			quantidade_14 = str(self.itens_selecionados_venda[item_14]['quantidade'])
			valor_14 = str(self.itens_selecionados_venda[item_14]['valor'])
			total_14 = (float(quantidade_14) * float(valor_14))
			total_14_form = str(round(total_14, 2))
			
			self.item_label_14.setText(item_14)
			self.unidade_selec_ed_14.setText(quantidade_14)
			self.valor_selec_ed_14.setText(valor_14)
			self.total_item_label_14.setText(total_14_form)
		except:
			pass

		try:	
			item_15 = lista_de_itens[14]
			quantidade_15 = str(self.itens_selecionados_venda[item_15]['quantidade'])
			valor_15 = str(self.itens_selecionados_venda[item_15]['valor'])
			total_15 = (float(quantidade_15) * float(valor_15))
			total_15_form = str(round(total_15, 2))
			
			self.item_label_15.setText(item_15)
			self.unidade_selec_ed_15.setText(quantidade_15)
			self.valor_selec_ed_15.setText(valor_15)
			self.total_item_label_15.setText(total_15_form)
		except:
			pass

		try:	
			item_16 = lista_de_itens[15]
			quantidade_16 = str(self.itens_selecionados_venda[item_16]['quantidade'])
			valor_16 = str(self.itens_selecionados_venda[item_16]['valor'])
			total_16 = (float(quantidade_16) * float(valor_16))
			total_16_form = str(round(total_16, 2))

			
			self.item_label_16.setText(item_16)
			self.unidade_selec_ed_16.setText(quantidade_16)
			self.valor_selec_ed_16.setText(valor_16)
			self.total_item_label_16.setText(total_16_form)
		except:
			pass
	
	def atualizar_quantidade_item_1(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[0] #trocar
		
		
		if self.unidade_selec_ed_1.text() == '.' or self.unidade_selec_ed_1.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_1.text() != '.' and self.unidade_selec_ed_1.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_1.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_1.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')
			
	def atualizar_quantidade_item_2(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[1]
		
		
		if self.unidade_selec_ed_2.text() == '.' or self.unidade_selec_ed_2.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_2.text() != '.' and self.unidade_selec_ed_2.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_2.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_2.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_3(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[2] #trocar
		
		
		if self.unidade_selec_ed_3.text() == '.' or self.unidade_selec_ed_3.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_3.text() != '.' and self.unidade_selec_ed_3.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_3.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_3.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_4(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[3] #trocar
		
		
		if self.unidade_selec_ed_4.text() == '.' or self.unidade_selec_ed_4.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_4.text() != '.' and self.unidade_selec_ed_4.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_4.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_4.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_5(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[4] #trocar
		
		
		if self.unidade_selec_ed_5.text() == '.' or self.unidade_selec_ed_5.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_5.text() != '.' and self.unidade_selec_ed_5.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_5.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_5.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_6(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[5] #trocar
		
		
		if self.unidade_selec_ed_6.text() == '.' or self.unidade_selec_ed_6.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_6.text() != '.' and self.unidade_selec_ed_6.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_6.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_6.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_7(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[6] #trocar
		
		
		if self.unidade_selec_ed_7.text() == '.' or self.unidade_selec_ed_7.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_7.text() != '.' and self.unidade_selec_ed_7.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_7.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_7.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_8(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[7] #trocar
		
		
		if self.unidade_selec_ed_8.text() == '.' or self.unidade_selec_ed_8.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_8.text() != '.' and self.unidade_selec_ed_8.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_8.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_8.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_9(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[8] #trocar
		
		
		if self.unidade_selec_ed_9.text() == '.' or self.unidade_selec_ed_9.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_9.text() != '.' and self.unidade_selec_ed_9.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_9.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_9.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_10(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[9] #trocar
		
		
		if self.unidade_selec_ed_10.text() == '.' or self.unidade_selec_ed_10.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_10.text() != '.' and self.unidade_selec_ed_10.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_10.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_10.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_11(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[10] #trocar
		
		
		if self.unidade_selec_ed_11.text() == '.' or self.unidade_selec_ed_11.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_11.text() != '.' and self.unidade_selec_ed_11.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_11.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_11.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_12(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[11] #trocar
		
		
		if self.unidade_selec_ed_12.text() == '.' or self.unidade_selec_ed_12.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_12.text() != '.' and self.unidade_selec_ed_12.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_12.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_12.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_13(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[12] #trocar
		
		
		if self.unidade_selec_ed_13.text() == '.' or self.unidade_selec_ed_13.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_13.text() != '.' and self.unidade_selec_ed_13.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_13.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_13.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_14(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[13] #trocar
		
		
		if self.unidade_selec_ed_14.text() == '.' or self.unidade_selec_ed_14.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_14.text() != '.' and self.unidade_selec_ed_14.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_14.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_14.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_15(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[14] #trocar
		
		
		if self.unidade_selec_ed_15.text() == '.' or self.unidade_selec_ed_15.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_15.text() != '.' and self.unidade_selec_ed_15.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_15.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_15.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_quantidade_item_16(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[15] #trocar
		
		
		if self.unidade_selec_ed_16.text() == '.' or self.unidade_selec_ed_16.text() == '':#trocar
			pass
		
		if self.unidade_selec_ed_16.text() != '.' and self.unidade_selec_ed_16.text() != '':#trocar

			self.itens_selecionados_venda[item]['quantidade'] = float(self.unidade_selec_ed_16.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_16.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_1(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[0] #trocar
		
		
		if self.valor_selec_ed_1.text() == '.' or self.valor_selec_ed_1.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_1.text() != '.' and self.valor_selec_ed_1.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_1.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_1.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_2(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[1] #trocar
		
		
		if self.valor_selec_ed_2.text() == '.' or self.valor_selec_ed_2.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_2.text() != '.' and self.valor_selec_ed_2.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_2.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_2.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_3(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[2] #trocar
		
		
		if self.valor_selec_ed_3.text() == '.' or self.valor_selec_ed_3.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_3.text() != '.' and self.valor_selec_ed_3.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_3.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_3.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_4(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[3] #trocar
		
		
		if self.valor_selec_ed_4.text() == '.' or self.valor_selec_ed_4.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_4.text() != '.' and self.valor_selec_ed_4.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_4.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_4.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_5(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[4] #trocar
		
		
		if self.valor_selec_ed_5.text() == '.' or self.valor_selec_ed_5.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_5.text() != '.' and self.valor_selec_ed_5.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_5.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_5.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_6(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[5] #trocar
		
		
		if self.valor_selec_ed_6.text() == '.' or self.valor_selec_ed_6.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_6.text() != '.' and self.valor_selec_ed_6.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_6.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_6.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_7(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[6] #trocar
		
		
		if self.valor_selec_ed_7.text() == '.' or self.valor_selec_ed_7.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_7.text() != '.' and self.valor_selec_ed_7.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_7.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_7.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_8(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[7] #trocar
		
		
		if self.valor_selec_ed_8.text() == '.' or self.valor_selec_ed_8.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_8.text() != '.' and self.valor_selec_ed_8.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_8.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_8.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_9(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[8] #trocar
		
		
		if self.valor_selec_ed_9.text() == '.' or self.valor_selec_ed_9.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_9.text() != '.' and self.valor_selec_ed_9.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_9.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_9.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_10(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[9] #trocar
		
		
		if self.valor_selec_ed_10.text() == '.' or self.valor_selec_ed_10.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_10.text() != '.' and self.valor_selec_ed_10.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_10.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_10.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_11(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[10] #trocar
		
		
		if self.valor_selec_ed_11.text() == '.' or self.valor_selec_ed_11.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_11.text() != '.' and self.valor_selec_ed_11.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_11.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_11.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_12(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[11] #trocar
		
		
		if self.valor_selec_ed_12.text() == '.' or self.valor_selec_ed_12.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_12.text() != '.' and self.valor_selec_ed_12.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_12.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_12.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_13(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[12] #trocar
		
		
		if self.valor_selec_ed_13.text() == '.' or self.valor_selec_ed_13.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_13.text() != '.' and self.valor_selec_ed_13.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_13.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_13.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_14(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[13] #trocar
		
		
		if self.valor_selec_ed_14.text() == '.' or self.valor_selec_ed_14.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_14.text() != '.' and self.valor_selec_ed_14.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_14.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_14.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_15(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[14] #trocar
		
		
		if self.valor_selec_ed_15.text() == '.' or self.valor_selec_ed_15.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_15.text() != '.' and self.valor_selec_ed_15.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_15.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_15.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')

	def atualizar_valor_item_16(self):
		lista_itens = list(self.itens_selecionados_venda.keys())#trocar
		item = lista_itens[15] #trocar
		
		
		if self.valor_selec_ed_16.text() == '.' or self.valor_selec_ed_16.text() == '':#trocar
			pass
		
		if self.valor_selec_ed_16.text() != '.' and self.valor_selec_ed_16.text() != '':#trocar

			self.itens_selecionados_venda[item]['valor'] = float(self.valor_selec_ed_16.text())#trocar
			
			#Calculando novamente o total do item 
			total_item = (self.itens_selecionados_venda[item]['quantidade'] * 
			self.itens_selecionados_venda[item]['valor'])
			total_item_form = round(total_item,2)
			
			self.total_item_label_16.setText(str(total_item_form))#trocar
			
			#Calculando novamente o teotal de todos os itens
			total = 0
			for item, info in self.itens_selecionados_venda.items():
				total_item = info['quantidade'] * info['valor']
				total += total_item
				total_form = round(total, 2)
				self.total_da_venda_label.setText(f'R$ {total_form}')


		
	def botao_deletar_item_1(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[0]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass
			
	def botao_deletar_item_2(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[1]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_3(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[2]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_4(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[3]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_5(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[4]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_6(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[5]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass
		

	def botao_deletar_item_7(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[6]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_8(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[7]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_9(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[8]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_10(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[9]]
				self.botao_lancar()
			else:
				print('Lista vazia')
				
		except:
			pass

	def botao_deletar_item_11(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[10]]
				self.botao_lancar()
			else:
				print('Lista vazia')
				
		except:
			pass

	def botao_deletar_item_12(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[11]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_13(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[12]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

	def botao_deletar_item_14(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[13]]
				self.botao_lancar()
			else:
				print('Lista vazia')
				
		except:
			pass

	def botao_deletar_item_15(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[14]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass
			
	def botao_deletar_item_16(self):
		try:
			lista = list(self.itens_selecionados_venda.keys())
			if lista:
				del self.itens_selecionados_venda[lista[15]]
				self.botao_lancar()
			else:
				print('Lista vazia')
		except:
			pass

#Faz a quantidade e valor debaixo do cabeçalho ser apenas digto e ponto
	def apenas_num_pont(self):
		for char in self.unidade_selec_ed_1.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_1.clear()
			else:
				a=0
		for char in self.valor_selec_ed_1.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_1.clear()
			else:
				a=0
		
		for char in self.unidade_selec_ed_2.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_2.clear()
			else:
				a=0
		for char in self.valor_selec_ed_2.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_2.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_3.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_3.clear()
			else:
				a=0
		for char in self.valor_selec_ed_3.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_3.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_4.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_4.clear()
			else:
				a=0
		for char in self.valor_selec_ed_4.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_4.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_5.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_5.clear()
			else:
				a=0
		for char in self.valor_selec_ed_5.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_5.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_6.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_6.clear()
			else:
				a=0
		for char in self.valor_selec_ed_6.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_6.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_7.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_7.clear()
			else:
				a=0
		for char in self.valor_selec_ed_7.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_7.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_8.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_8.clear()
			else:
				a=0
		for char in self.valor_selec_ed_8.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_8.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_9.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_9.clear()
			else:
				a=0
		for char in self.valor_selec_ed_9.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_9.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_10.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_10.clear()
			else:
				a=0
		for char in self.valor_selec_ed_10.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_10.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_11.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_11.clear()
			else:
				a=0
		for char in self.valor_selec_ed_11.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_11.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_12.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_12.clear()
			else:
				a=0
		for char in self.valor_selec_ed_12.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_12.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_13.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_13.clear()
			else:
				a=0
		for char in self.valor_selec_ed_13.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_13.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_14.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_14.clear()
			else:
				a=0
		for char in self.valor_selec_ed_14.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_14.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_15.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_15.clear()
			else:
				a=0
		for char in self.valor_selec_ed_15.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_15.clear()
			else:
				a=0

		for char in self.unidade_selec_ed_16.text():
			if not char.isdigit() and char != '.':
				self.unidade_selec_ed_16.clear()
			else:
				a=0
		for char in self.valor_selec_ed_16.text():
			if not char.isdigit() and char != '.':
				self.valor_selec_ed_16.clear()
			else:
				a=0

	
#Botao finalizar venda, salva os itens no json historico de vendas		
	def salvar_itens_selecionados_venda_json(self):
		self.carregar_historico_vendas()
		self.carregar_estoque()
		
		if self.itens_selecionados_venda:
			total_venda = 0
			custo_venda = 0
		
			#Calcula o total da venda
			for item, info in self.itens_selecionados_venda.items():
			
				total_item = (self.itens_selecionados_venda[item]['quantidade']
				* self.itens_selecionados_venda[item]['valor'])
			
				total_venda += total_item
		
			#Calcula lucro total da venda
			for item, info in self.itens_selecionados_venda.items():
				custo_item = (self.estoque[item]['custo'] *
				self.itens_selecionados_venda[item]['quantidade'])
			
				custo_venda += custo_item
		
			total_venda_form = round(total_venda, 2)
		
			custo_venda_form = round(custo_venda, 2)
		
			lucro_venda = (total_venda - custo_venda)	
			lucro_venda_form = round(lucro_venda, 2)	
		
			resposta = QMessageBox.information(self, 'Finalização de venda',
			f'''<p>    Total: R$ {total_venda_form}    </p>
			<p>    Custo: R$ {custo_venda_form}    </p>
			<p>    LB : R$ {lucro_venda_form}    </p>
			<p> </p>
			<p>    Confirmar (Yes) / Sair (No)</p>''',
			QMessageBox.StandardButton.Yes |\
			QMessageBox.StandardButton.No, 
			QMessageBox.StandardButton.Yes)
			
			#COnfirmando cria o dicionário de historico de vendas
			'''dic = {'cod': 'itens':{'item': {'quantidade': 1, 'valor': 1, 'custo': 0.5}, info: {'data': ---}'''
			
			if resposta == QMessageBox.StandardButton.Yes:
				#Define o local da data e da hora e do dia
				locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
				
				data_venda = datetime.now().strftime('%d-%m-%y')#DIA MES ANO
				dia_da_semana = datetime.now().strftime('%A')
				mes = datetime.now().strftime('%B')
				mes_ano = datetime.now().strftime('%m-%y')
				ano = datetime.now().strftime('%Y')
				codigo_venda = str(self.gerar_proximo_codigo_venda())
				
				venda = {}
				info = {}
				itens = self.itens_selecionados_venda #{}
				
				info['data'] = data_venda
				info['dia'] = dia_da_semana
				info['mes'] = mes
				info['mes_ano'] = mes_ano
				info['ano'] = ano
				venda['itens'] = itens
				venda['info'] = info
				self.historico_vendas[codigo_venda] = venda
				
				#Salva os dados da venda no json historico de vendas
				self.salvar_historico_vendas_json()
				
			#Subtrair as quantidades no estoque
				for item, info in self.itens_selecionados_venda.items():
					self.estoque[item]['quantidade'] -= self.itens_selecionados_venda[item]['quantidade']
				
				
				self.salvar_estoque()
				self.carregar_estoque()
				self.itens_selecionados_venda = {}
				self.botao_lancar()
				self.botao_click_barra()


				
				

		else:
			QMessageBox.warning(self, 'Venda vazia',
			'ATENÇÃO, A SUA PÁGINA DE VENDAS DEVE TER PELO MENOS 1 ITEM!!!',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
			
		
	def carregar_estoque(self):
		try:
			with open('base_data/estoque.json', 'r') as file:
				content = file.read()
				if content:
					self.estoque.update(json.loads(content))
					
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Não foi possível carregar o seu estoque')		

	def carregar_historico_vendas(self):
		try:
			with open('base_data/historico_vendas.json', 'r') as file:
				content = file.read()
				if content:
					self.historico_vendas.update(json.loads(content))
					
		except (FileNotFoundError, json.JSONDecodeError):
			print('Histórico de vendas vazio')
			
	def carregar_preco_sugerido(self):
		try:
			with open('base_data/preco_sugerido.json', 'r') as file:
				content = file.read()
				if content:
					self.preco_sugerido_dic.update(json.loads(content))
		except:
			pass
			
	def salvar_historico_vendas_json(self):
		with open('base_data/historico_vendas.json', 'w') as file:
			json.dump(self.historico_vendas, file)		
		
	def salvar_estoque(self):
		with open('base_data/estoque.json', 'w') as file:
			json.dump(self.estoque, file)
			
	def apenas_num_pont_quantidade(self):
		for char in self.quantidade_item_ed.text():
			if not char.isdigit() and char != '.':
				self.quantidade_item_ed.clear()
			else:
				a=0		
		
	def apenas_num_pont_valor(self):
		for char in self.valor_item_ed.text():
			if not char.isdigit() and char != '.':
				self.valor_item_ed.clear()
			else:
				a=0	
	
	def total_da_venda_entrada(self):	
		novo_total = self.total_da_venda_edit.text()
		total_atual = 0
	
		for item, info in self.itens_selecionados_venda.items():
			total_atual  += info['quantidade'] * info['valor']
		
		if (novo_total != '' 
		and novo_total != '.' 
		and novo_total != '0' 
		and novo_total != '0.0'
		and novo_total != '0.'):
			try:
				diferenca = float(novo_total) - float(total_atual)
				porcentagem = (float(diferenca) / float(total_atual))
			
				for item, info in self.itens_selecionados_venda.items():
					novo_valor_do_item = ((info['valor'] * float(porcentagem)) + (info['valor']))
					novo_valor_do_item_form = round(novo_valor_do_item, 4)
					
					info['valor'] = novo_valor_do_item_form
				print(f' Original 1: {self.itens_selecionados_venda}')
			except ValueError:
				QMessageBox.warning(self, 'Formato não suportado',
				'''<p>Atenção o formado inserido no Total de vendas não é suportado!!!</p>
				<p> Use apenas digitos e pontos, evite errors!!!!!</p>''',
				QMessageBox.StandardButton.Ok,
				QMessageBox.StandardButton.Ok)
				self.total_da_venda_edit.clear()

		if (novo_total == ''
		or novo_total == '.'
		or novo_total == '0'
		or novo_total == '0.0'
		or novo_total == '0.'
		or novo_total == '0.00'):
			
			pass
			
				
		self.botao_lancar()
			



		self.itens_selecionados_venda_total = self.itens_selecionados_venda

	#Quando o botao for clicado, o cursor voltará para a barra de pesquisa
	def botao_click_barra(self):
		self.barra_pesquisa_item_ed.clear()
		self.barra_pesquisa_item_ed.setFocus()

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Nova_venda()
	sys.exit(app.exec())
