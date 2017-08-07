#!/usr/bin/python3
import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QComboBox, QDoubleSpinBox, QGridLayout

class Form(QDialog):

	def __init__(self, parent=None):
		super().__init__(parent)
		date = self.getdata()
		rates = sorted(self.rates.keys())
		dateLabel = QLabel(date)

		self.fromComboBox = QComboBox()
		self.fromComboBox.addItems(rates)

		self.fromSpinBox = QDoubleSpinBox()
		self.fromSpinBox.setRange(0.01, 100000.00)
		self.fromSpinBox.setValue(1.000)
		self.toComboBox = QComboBox()
		self.toComboBox.addItems(rates)
		self.toLabel = QLabel("1.000")
		grid = QGridLayout()
		grid.addWidget(dateLabel, 0, 0)
		grid.addWidget(self.fromComboBox, 1, 0)
		grid.addWidget(self.fromSpinBox, 1, 1)
		grid.addWidget(self.toComboBox, 2, 0)
		grid.addWidget(self.toLabel, 2, 1)
		self.setLayout(grid)
		self.fromComboBox.currentIndexChanged.connect(self.updateUi)
		self.toComboBox.currentIndexChanged.connect(self.updateUi)
		self.fromSpinBox.valueChanged.connect(self.updateUi)
		self.setWindowTitle("Currency")

	def updateUi(self):
		to = str(self.toComboBox.currentText())
		from_ = str(self.fromComboBox.currentText())
		amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
		self.toLabel.setText("{0:.{1}f}".format(amount, 3))

	def getdata(self):
		self.rates = {}
		try:
			readfile = requests.get('http://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json')
			data = readfile.json()
			codes = data['seriesDetail']
			date = data['observations'][-1]['d']
			for code in codes:
				label = data['seriesDetail']['{}'.format(code)]['description']
				self.rates[label.split("to")[0]] =  data['observations'][-1]['{}'.format(code)]['v']
			self.rates["Canadian dollar"] = 1.000
			return "Exchange Rates Date: " + date
		except Exception as e:
			return "Failed to download:\n{}".format(e)

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

