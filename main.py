from PyQt5.QtWidgets import QApplication
from GUI.loginscreenWidget import LoginScreenWidget
from GUI.mailboxMainWindow import MailBoxMainWindow
from GUI.contentWidget import ContentWidget
from GUI.createmessageWidget import CreateMessage
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginScreenWidget()

    sys.exit(app.exec_())
