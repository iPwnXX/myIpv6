from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from upLoader import upLoader

import example_ui as ui


class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # edit part
        self.init_ui()
        self.textEdit_period.textChanged.connect(self.period_changed)
        UpLoader.set_info_funcs([self.last_checked_update,
                                 self.last_upload_update])

    def init_ui(self):
        self.setWindowTitle('IpUploader')
        self.label_ipv6.setText(UpLoader.MyIpv6)
        self.textEdit_period.setText(str(UpLoader.cycleTime))
        self.label_last_update.setText(UpLoader.last_time_upload)
        self.label_last_check.setText(UpLoader.last_time_checked)

    def period_changed(self, text):
        UpLoader.set_check_period(int(text))

    def last_checked_update(self):
        self.label_last_check.setText(UpLoader.last_time_checked)

    def last_upload_update(self):
        self.label_last_update.setText(UpLoader.last_time_upload)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpLoader = upLoader(cycle_time=5, verbose=True, gui_enable=True)
    window = Main()
    window.show()
    sys.exit(app.exec_())
