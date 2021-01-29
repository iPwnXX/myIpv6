# recompile to exe: pyinstaller -w -i pic/code.ico ./src_code/startUpLoader.py
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


if __name__ == '__main__':
    git_dir = '../../'
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
    a1 = QAction('&显示(Show)', triggered=w.show)


    def quitApp():
        w.show()  # w.hide() #隐藏
        re = QMessageBox.question(w, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
            tp.setVisible(False)


    a2 = QAction('&退出(Exit)', triggered=quitApp)  # 直接退出可以用qApp.quit
    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()
    # 信息提示
    # 参数1：标题
    # 参数2：内容
    # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
    # tp.showMessage('IPupLoader', 'tpContent', icon=0)
    #
    #
    # def message():
    #     print("弹出的信息被点击了")
    #
    #
    # tp.messageClicked.connect(message)


    def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            w.show()
        # print("系统托盘的图标被点击了")


    tp.activated.connect(act)
    # -------------------- 托盘结束 ----------
    sys.exit(app.exec_())
