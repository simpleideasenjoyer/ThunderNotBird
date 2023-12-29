from PyQt5.QtWidgets import QWidget, QMainWindow
from .ui_loginscreenWidget import Ui_loginScreenWidget
from .ui_mailboxMainWindow import Ui_ThunderNOTBird
from PyQt5.QtCore import pyqtSignal
import imaplib
import sys
from .utils.logic import SendEmail, ReceiveEmail



class LoginScreenWidget(QWidget, Ui_loginScreenWidget):

    def __init__(self):
        super().__init__()
        self.uiLogin = Ui_loginScreenWidget()
        self.uiLogin.setupUi(self)
        self.uiLogin.loginButton.clicked.connect(self.check_login)
        self.uiLogin.exitButton.clicked.connect(self.exit)


    def exit(self):
        sys.exit()
