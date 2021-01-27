from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import example_ui as ui


class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # edit part
        self.initUI()

    def initUI(self):
        self.setWindowTitle('IpUploader')
        self.label_ipv6.setText('')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
