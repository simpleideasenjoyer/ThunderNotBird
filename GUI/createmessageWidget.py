from .ui_createmessageWidget import Ui_CreateMessageWidget
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QWidget,
    QFileDialog,
    QListWidgetItem,
)
from PyQt5.QtCore import Qt, pyqtSignal, QFileInfo
from .utils.logic import SendEmail


class CreateMessage(QWidget, Ui_CreateMessageWidget):
    def __init__(self):
        super().__init__()
        self.uiCreateMessage = Ui_CreateMessageWidget()
        self.uiCreateMessage.setupUi(self)
        self.attachments = []
        self.uiCreateMessage.toLineEdit.clear()
        self.uiCreateMessage.subjectLineEdit.clear()
        self.uiCreateMessage.messageBoxTextEdit.clear()
        self.uiCreateMessage.sendButton.clicked.connect(self.send_mail)

    def get_message_data(self, createMessageObject):
        self.smtpObject = SendEmail(
            createMessageObject.emailData, createMessageObject.passwordData
        )

    def send_mail(self):
        self.smtpObject.create_message(
            self.uiCreateMessage.subjectLineEdit.text(),
            self.uiCreateMessage.messageBoxTextEdit.toPlainText(),
            self.uiCreateMessage.toLineEdit.text(),
        )
        for attachmentPath in self.attachments:
            self.smtpObject.attachment(attachmentPath)

        self.smtpObject.send_mail()
        self.close()

    def add_attachment(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePaths, _ = QFileDialog.getOpenFileNames(
            self, "Wybierz pliki", "", "Wszystkie pliki (*);;Pliki tekstowe (*.txt)"
        )
        if filePaths:
            self.attachments.extend(filePaths)
            self.update_attachment_list()


    def update_attachment_list(self):
        self.uiCreateMessage.attachmentListWidget.clear()
        for filePaths in self.attachments:
            filename = QFileInfo(filePaths).fileName()
            item = QListWidgetItem(filename)
            self.uiCreateMessage.attachmentListWidget.addItem(item)
