from .ui_createmessageWidget import Ui_CreateMessageWidget
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QWidget,
    QFileDialog,
    QListWidgetItem,
    QMessageBox,
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
        self.uiCreateMessage.ccLineEdit.clear()
        self.uiCreateMessage.bccLineEdit.clear()
        self.uiCreateMessage.subjectLineEdit.clear()
        self.uiCreateMessage.messageBoxTextEdit.clear()
        self.uiCreateMessage.sendButton.clicked.connect(self.send_mail)
        self.uiCreateMessage.addAttachmentButton.clicked.connect(self.add_attachment)
        self.uiCreateMessage.attachmentListWidget.itemDoubleClicked.connect(
            self.remove_attachment_item
        )
        self._smtpObject: SendEmail | None = None

    def get_message_data(self, createMessageObject) -> None:
        """Receive the authenticated ReceiveEmail object and prepare an SMTP sender."""
        self._smtpObject = SendEmail(
            createMessageObject.emailData,
            createMessageObject.passwordData,
            smtpServer=createMessageObject.smtpServer,
            smtpPort=createMessageObject.smtpPort,
            smtpSsl=createMessageObject.smtpSsl,
        )

    def send_mail(self) -> None:
        if self._smtpObject is None:
            QMessageBox.warning(self, "Send", "Not connected to mail server.")
            return

        to = self.uiCreateMessage.toLineEdit.text().strip()
        subject = self.uiCreateMessage.subjectLineEdit.text().strip()
        body = self.uiCreateMessage.messageBoxTextEdit.toPlainText()
        cc = self.uiCreateMessage.ccLineEdit.text().strip()
        bcc = self.uiCreateMessage.bccLineEdit.text().strip()

        if not to:
            QMessageBox.warning(self, "Validation", "The 'To' field cannot be empty.")
            return
        if not subject:
            QMessageBox.warning(self, "Validation", "The 'Subject' field cannot be empty.")
            return

        try:
            self._smtpObject.create_message(subject, body, to)
            if cc:
                self._smtpObject.msg["Cc"] = cc
            if bcc:
                self._smtpObject.msg["Bcc"] = bcc
            for attachment_path in self.attachments:
                self._smtpObject.attachment(attachment_path)
            self._smtpObject.send_mail()
            QMessageBox.information(self, "Send", "Message sent successfully.")
            self._reset_form()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Send failed", f"Could not send message:\n{e}")

    def add_attachment(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePaths, _ = QFileDialog.getOpenFileNames(
            self, "Select files", "", "All files (*);;Text files (*.txt)", options=options
        )
        if filePaths:
            self.attachments.extend(filePaths)
            self._update_attachment_list()

    def remove_attachment_item(self, item: QListWidgetItem) -> None:
        row = self.uiCreateMessage.attachmentListWidget.row(item)
        if 0 <= row < len(self.attachments):
            del self.attachments[row]
            self._update_attachment_list()

    def _update_attachment_list(self) -> None:
        self.uiCreateMessage.attachmentListWidget.clear()
        for path in self.attachments:
            filename = QFileInfo(path).fileName()
            self.uiCreateMessage.attachmentListWidget.addItem(QListWidgetItem(filename))

    def _reset_form(self) -> None:
        self.attachments.clear()
        self.uiCreateMessage.toLineEdit.clear()
        self.uiCreateMessage.ccLineEdit.clear()
        self.uiCreateMessage.bccLineEdit.clear()
        self.uiCreateMessage.subjectLineEdit.clear()
        self.uiCreateMessage.messageBoxTextEdit.clear()
        self._update_attachment_list()

