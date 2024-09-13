import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
QPushButton, QGridLayout, QMessageBox)
from PyQt6.QtCore import (Qt, QThread, pyqtSignal)
from PyQt6.QtGui import QPixmap, QFont
import time

class WorkerThread(QThread):
	cotas_sinal = pyqtSignal(int)
	def __init__(self, valor_cota, div_mensal, aporte_inicial,
		aporte_mensal, meses_totais):
		
		super().__init__()
		self.valor_cota = valor_cota
		self.div_mensal = div_mensal
		self.aporte_inicial = aporte_inicial
		self.aporte_mensal = aporte_mensal
		self.meses_totais = meses_totais
		
	def run(self):
		self.carteira = 0
		self.carteira += self.aporte_inicial		
		
		
		self.rendimento = 0

		self.quantidade_cotas = 0
		
		for i in range(self.meses_totais):
			self.carteira += self.aporte_mensal
			
			self.quantidade_cotas = (self.carteira / self.valor_cota)
			self.quantidade_cotas_form = int(self.quantidade_cotas)
			
			self.rendimento = float(self.quantidade_cotas_form * self.div_mensal)
			self.carteira += self.rendimento
			self.cotas_sinal.emit(self.quantidade_cotas_form)
			
		


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initializeUI()
		
	def initializeUI(self):
		self.setMinimumSize(200, 200)
		self.setWindowTitle('Simulador Fi')
		self.setUpMainWindow()
		self.show()
		
	def setUpMainWindow(self):
		simulador_label = QLabel('Simulador')
		simulador_label.setFont(QFont('Arial', 18))
		
		valor_cota_label = QLabel('Valor da Cota: R$')
		valor_cota_label.setFont(QFont('Arial', 10))
		
		dividendo_mensal_label = QLabel('Dividendo Mensal: R$')
		dividendo_mensal_label.setFont(QFont('Arial', 10))
		
		informacao_titulo_label = QLabel('Informações do seu plano de investimento')
		informacao_titulo_label.setFont(QFont('Arial', 16))
			
		montante_aplicado_mes1_label = QLabel('Montante Aplicado 1° mês: R$')
		montante_aplicado_mes1_label.setFont(QFont('Arial', 10))
		
		aporte_mensal_label = QLabel('Aporte Mensal: R$')
		aporte_mensal_label.setFont(QFont('Arial', 10))
		
		meses_totais_label = QLabel('Meses Totais Do Regime:')
		meses_totais_label.setFont(QFont('Arial', 10))
		
		self.valor_cota_ed = QLineEdit('163')
		self.valor_cota_ed.setFixedSize(90, 20)
		
		self.dividendo_mensal_ed = QLineEdit('1.1')
		self.dividendo_mensal_ed.setFixedSize(90, 20)
		
		self.montante_ed = QLineEdit('0')
		self.montante_ed.setFixedSize(150, 20)
		
		self.aporte_mensal_ed = QLineEdit('1000')
		self.aporte_mensal_ed.setFixedSize(90, 20)
		
		self.quantidade_meses_ed = QLineEdit('1')
		self.quantidade_meses_ed.setFixedSize(90, 20)
		
		botao_simular = QPushButton('Simular')
		botao_simular.clicked.connect(self.iniciar_calculo)
		
		resultado_label = QLabel('Resultado')
		resultado_label.setFont(QFont('Arial', 16))
		
		self.meses_label = QLabel('--- meses')
		self.meses_label.setFont(QFont('Arial', 10))
		
		self.cotas_label = QLabel('--- cotas finais')
		self.cotas_label.setFont(QFont('Arial', 10))
		
		self.montante_label = QLabel('R$ --- montante')
		self.montante_label.setFont(QFont('Arial', 10))
		
		self.rendimento_mensal_label = QLabel('R$ --- de renda mensal')
		self.montante_label.setFont(QFont('Arial', 10))
		
		main_grid = QGridLayout()
		main_grid.addWidget(simulador_label, 0, 0)
		main_grid.addWidget(valor_cota_label, 1, 0)
		main_grid.addWidget(self.valor_cota_ed, 1, 1)
		main_grid.addWidget(dividendo_mensal_label, 2, 0)
		main_grid.addWidget(self.dividendo_mensal_ed, 2, 1)
		main_grid.addWidget(informacao_titulo_label, 3, 0, 1, 2)
		main_grid.addWidget(montante_aplicado_mes1_label, 4, 0)
		main_grid.addWidget(self.montante_ed, 4, 1)
		main_grid.addWidget(aporte_mensal_label, 5, 0)
		main_grid.addWidget(self.aporte_mensal_ed, 5, 1)
		main_grid.addWidget(meses_totais_label, 6, 0)
		main_grid.addWidget(self.quantidade_meses_ed, 6, 1)
		main_grid.addWidget(botao_simular, 7, 0, 1, 2)
		main_grid.addWidget(resultado_label, 8, 0)
		main_grid.addWidget(self.meses_label, 9, 0)
		main_grid.addWidget(self.cotas_label, 10, 0)
		main_grid.addWidget(self.montante_label, 11, 0)
		main_grid.addWidget(self.rendimento_mensal_label, 12, 0)
		
		self.setLayout(main_grid)
		

	def iniciar_calculo(self):
		try:
			valor_cota_e = float(self.valor_cota_ed.text())
			div_mensal_e = float(self.dividendo_mensal_ed.text())
			aporte_inicial_e = float(self.montante_ed.text())
			aporte_mensal_e = float(self.aporte_mensal_ed.text())
			meses_totais_e = int(self.quantidade_meses_ed.text())
			
			

		
		
		
		except:
			QMessageBox.warning(self, 'Error de entrada',
			f'''<p> Certifique-se que todos os dados sejam numeros</p>
				<p> Certifique-se que os meses seja um numero inteiro<\p>
				<p> Certifique-se de usar '.'(ponto) ao invés de virgula<\p>
				''',
			QMessageBox.StandardButton.Ok,
			QMessageBox.StandardButton.Ok)
		
		self.worker_thread = WorkerThread(
			valor_cota = valor_cota_e,
			div_mensal = div_mensal_e,
			aporte_inicial = aporte_inicial_e,
			aporte_mensal = aporte_mensal_e,
			meses_totais = meses_totais_e)	
		self.worker_thread.cotas_sinal.connect(self.resultado)	
		self.worker_thread.start()
		
	def resultado(self, value):
		quantidade_cotas = value
		
		meses = self.quantidade_meses_ed.text()
		cotas = quantidade_cotas
		montante = (float(self.valor_cota_ed.text()) * quantidade_cotas)
		renda = (float(self.dividendo_mensal_ed.text()) * quantidade_cotas)
		renda_f = round(renda, 2)
		self.meses_label.setText(str(f'{str(meses)} meses'))
		self.cotas_label.setText(str(f'{str(cotas)} cotas finais'))
		self.montante_label.setText(str(f' R${montante} montante'))
		self.rendimento_mensal_label.setText(str(f'R$ {renda_f} de renda mensal'))
		
		
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())
