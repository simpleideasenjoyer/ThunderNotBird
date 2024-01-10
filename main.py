from PyQt5.QtWidgets import QApplication
from GUI.loginscreenWidget import LoginScreenWidget
from GUI.mailboxMainWindow import MailBoxMainWindow
from GUI.contentWidget import ContentWidget
from GUI.createmessageWidget import CreateMessage
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginScreenWidget()
    content = ContentWidget()
    createMessage = CreateMessage()
    mainWindow = MailBoxMainWindow()

    login.show()
    login.objectTransfer.connect(mainWindow.signal_receiver)
    login.loginSuccessful.connect(mainWindow.show)

    mainWindow.contentObject.connect(content.display_content)
    mainWindow.openContent.connect(content.show)

    mainWindow.openCreateMessage.connect(createMessage.show)
    mainWindow.createMessageObject.connect(createMessage.get_message_data)

    sys.exit(app.exec_())