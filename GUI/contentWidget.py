from PyQt5.QtWidgets import QWidget, QMainWindow
from .ui_contentWidget import Ui_ContentWidget
from PyQt5.QtCore import pyqtSignal
from html import unescape


class ContentWidget(QWidget, Ui_ContentWidget):
    def __init__(self):
        super().__init__()
        self.uiContentWidget = Ui_ContentWidget()
        self.uiContentWidget.setupUi(self)

    def display_content(self, emailObject):
        if emailObject.get_content_type() == "text/html":
            mail = emailObject.get_payload(decode=True)
            if isinstance(mail, bytes):
                mail = mail.decode("utf-8")
            mail = unescape(mail)
            self.uiContentWidget.contentWebEngineView.setHtml(mail)
        elif emailObject.get_content_type() == "multipart/alternative":
            for part in emailObject.get_payload():
                if part.get_content_type() == "text/html":
                    mail = part.get_payload(decode=True)
                    if isinstance(mail, bytes):
                        mail = mail.decode("utf8")
                    mail = unescape(mail)
                    self.uiContentWidget.contentWebEngineView.setHtml(mail)
        elif emailObject.get_content_type() == "text/plain":
            mail = emailObject.get_payload()
            if isinstance(mail, bytes):
                mail = mail.decode("utf-8")
            self.uiContentWidget.contentWebEngineView.setHtml(mail)
