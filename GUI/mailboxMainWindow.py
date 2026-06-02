from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from .ui_mailboxMainWindow import Ui_ThunderNOTBird
import sys


class MailBoxMainWindow(QMainWindow, Ui_ThunderNOTBird):
    openContent = pyqtSignal()
    contentObject = pyqtSignal(object)
    openCreateMessage = pyqtSignal()
    createMessageObject = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.uiMailBox = Ui_ThunderNOTBird()
        self.uiMailBox.setupUi(self)
        self.uiMailBox.mailTableWidget.setColumnWidth(0, 150)
        self.uiMailBox.mailTableWidget.setColumnWidth(1, 300)
        self.uiMailBox.mailTableWidget.setColumnWidth(2, 150)
        self.uiMailBox.mailTableWidget.itemDoubleClicked.connect(self.show_content)

        self.uiMailBox.createMessageToolButton.clicked.connect(self.open_create_message)
        self.uiMailBox.actionCreate_a_new_message.triggered.connect(self.open_create_message)
        self.uiMailBox.actionDelete_message.triggered.connect(self.delete_selected_message)
        self.uiMailBox.actionExit.triggered.connect(lambda: sys.exit())

        self.uiMailBox.foldersListWidget.itemClicked.connect(self.on_folder_selected)

        self._imapObject = None
        self._current_folder = "INBOX"
        self._inbox = []  # list of (uid, email_message)

    def signal_receiver(self, imapObject) -> None:
        """Receive the authenticated ReceiveEmail object from the login screen."""
        self._imapObject = imapObject
        self._load_folders()
        self.show_folder("INBOX")

    def _load_folders(self) -> None:
        """Populate the folder list widget from the IMAP server."""
        try:
            folders = self._imapObject.get_folders()
        except Exception as e:
            QMessageBox.warning(self, "Folders", f"Could not load folder list:\n{e}")
            return

        self.uiMailBox.foldersListWidget.clear()
        for folder in folders:
            self.uiMailBox.foldersListWidget.addItem(folder)

    def on_folder_selected(self, item) -> None:
        self.show_folder(item.text())

    def show_folder(self, folder_name: str) -> None:
        """Load and display messages from *folder_name*."""
        if self._imapObject is None:
            return

        self._current_folder = folder_name

        try:
            self._inbox = self._imapObject.mailbox_printer(folder_name)
            unread_uids = self._imapObject.get_unread_uids(folder_name)
        except Exception as e:
            QMessageBox.critical(self, "Mail", f"Could not load messages:\n{e}")
            return

        table = self.uiMailBox.mailTableWidget
        table.setRowCount(0)

        bold_font = QFont()
        bold_font.setBold(True)

        row = 0
        for uid, mail in self._inbox:
            table.insertRow(row)
            is_unread = uid in unread_uids

            from_item = QTableWidgetItem(mail["From"] or "")
            subject_item = QTableWidgetItem(
                self._imapObject.decode_subject(mail["Subject"] or "")
            )
            date_item = QTableWidgetItem(mail["Date"] or "")

            if is_unread:
                from_item.setFont(bold_font)
                subject_item.setFont(bold_font)
                date_item.setFont(bold_font)

            table.setItem(row, 0, from_item)
            table.setItem(row, 1, subject_item)
            table.setItem(row, 2, date_item)
            row += 1

    def show_content(self, item) -> None:
        row = item.row()
        if row < len(self._inbox):
            _uid, mail = self._inbox[row]
            self.openContent.emit()
            self.contentObject.emit(mail)

    def open_create_message(self) -> None:
        if self._imapObject is None:
            return
        self.openCreateMessage.emit()
        self.createMessageObject.emit(self._imapObject)

    def delete_selected_message(self) -> None:
        """Delete the currently selected message after user confirmation."""
        selected = self.uiMailBox.mailTableWidget.currentRow()
        if selected < 0 or selected >= len(self._inbox):
            return

        reply = QMessageBox.question(
            self,
            "Delete message",
            "Are you sure you want to delete the selected message?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        uid, _ = self._inbox[selected]
        try:
            self._imapObject.delete_message(self._current_folder, uid)
        except Exception as e:
            QMessageBox.critical(self, "Delete", f"Could not delete message:\n{e}")
            return

        self.show_folder(self._current_folder)
