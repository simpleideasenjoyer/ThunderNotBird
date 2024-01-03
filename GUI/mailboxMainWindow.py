from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from .ui_mailboxMainWindow import Ui_ThunderNOTBird
import sys
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import mimetypes
from email import encoders, message_from_bytes
import ssl
import imaplib
from html import unescape
import base64
import quopri


class MailBoxMainWindow(QMainWindow, Ui_ThunderNOTBird):
    openContent = pyqtSignal()
    contentObject = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.uiMailBox = Ui_ThunderNOTBird()
        self.uiMailBox.setupUi(self)
        self.uiMailBox.mailTableWidget.setColumnWidth(0, 150)
        self.uiMailBox.mailTableWidget.setColumnWidth(1, 300)
        self.uiMailBox.mailTableWidget.setColumnWidth(2, 150)
        self.uiMailBox.mailTableWidget.itemDoubleClicked.connect(self.show_content)

