import sys
from PySide.QtCore import *
from PySide.QtGui import *
import urllib2

"""
author: Atif Imam
"""

class Form(QDialog):

    # inialization of QDialog
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # grab latest rates and date
        date = self.getdata()
        rates = sorted(self.rates.keys())

        # data set
        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 1000000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")

        # theme layout
        grid = QGridLayout()
        # must specify position with grid layout
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.setWindowTitle("Currency Convertor")

        # behvaiour signals
        self.connect(self.fromComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.toComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)
    def setIcon(self):
        '''function to set icon'''
        appIcon=QIcon('currency2.png')
        self.setWindowIcon(appIcon)
        

    def updateUi(self):

        # update the GUI when new country is selected along with conversion
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

    def getdata(self):

        self.rates = {}
        # grab the data set from the the Bank of Canada exchange
        try:
            date = "Unknown"
            fh = urllib2.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")

            # iterate through file
            for line in fh:
                line = line.rstrip()
                if not line or line.startswith(("#", "Closing")):
                    continue

                fields = line.split(",")

                if line.startswith("Date "):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[fields[0]] = value

                    except ValueError:
                        pass

            return "Exchange rates date: " + date

        except Exception, e:
            return "Failed to download: \n%s" % e

# initialize application
app = QApplication(sys.argv)
form = Form()
form.setIcon()
form.show()
app.exec_()