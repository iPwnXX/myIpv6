# recompile to exe: pyinstaller -w -i pic/code.ico ./src/MinStartUpLoader.py
# -w: no console shown.  -F: compress to single exe file. May fail.

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
        if text != '':
            try:
                text_int = int(text)
                if 5 <= text_int <= 60*60:
                    UpLoader.set_check_period(text_int)

            except ValueError:
                pass

    def last_checked_update(self):
        self.label_ipv6.setText(UpLoader.MyIpv6)
        self.label_last_check.setText(UpLoader.last_time_checked)

    def last_upload_update(self):
        self.label_last_update.setText(UpLoader.last_time_upload)


def get_git_repos_relative_dir():
    import os
    split_path = os.getcwd().split('\\')
    git_dir_upper_level = len(split_path) - (split_path.index('myIpv6')+1)
    git_dir = ''
    for i in range(git_dir_upper_level):
        git_dir += '../'

    return git_dir


if __name__ == '__main__':
    git_dir = get_git_repos_relative_dir()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    UpLoader = upLoader(git_dir=git_dir, cycle_time=5, verbose=True, gui_enable=True)
    window = Main()
    window.show()

    # -------------------- 托盘开始 ----------
    # 在系统托盘处显示图标
    w = window
    tp = QSystemTrayIcon(w)
    tp.setIcon(QIcon(git_dir+'pic/favicon-96x96.png'))
    # 设置系统托盘图标的菜单
    a1 = QAction('&Show', triggered=w.show)


    def quitApp():
        w.show()  # w.hide() #隐藏
        re = QMessageBox.question(w, "prompt", "Exit Program ?", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            tp.setVisible(False)


    a2 = QAction('&(Exit)', triggered=quitApp)  # 直接退出可以用qApp.quit
    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()

    def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            w.show()


    tp.activated.connect(act)
    # -------------------- 托盘结束 ----------
    sys.exit(app.exec_())
