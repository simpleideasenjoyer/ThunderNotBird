from PyQt5.QtWidgets import QWidget, QListWidgetItem
from .ui_contentWidget import Ui_ContentWidget
from PyQt5.QtCore import pyqtSignal
from email.header import decode_header as _decode_header
from html import unescape
import html


class ContentWidget(QWidget, Ui_ContentWidget):
    def __init__(self):
        super().__init__()
        self.uiContentWidget = Ui_ContentWidget()
        self.uiContentWidget.setupUi(self)

    @staticmethod
    def _decode_header_value(value: str) -> str:
        if not value:
            return ""
        parts = _decode_header(value)
        decoded = []
        for part, charset in parts:
            if isinstance(part, bytes):
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            else:
                decoded.append(part)
        return "".join(decoded)

    def display_content(self, emailObject) -> None:
        subject = self._decode_header_value(emailObject.get("Subject", ""))
        self.uiContentWidget.subjectLineEdit.setText(subject)
        self.uiContentWidget.fromLineEdit.setText(emailObject.get("From", ""))

        html_body = None
        plain_body = None
        attachments = []

        if emailObject.is_multipart():
            for part in emailObject.walk():
                ct = part.get_content_type()
                cd = str(part.get("Content-Disposition", ""))
                filename = part.get_filename()
                if filename or "attachment" in cd:
                    attachments.append(self._decode_header_value(filename or "attachment"))
                    continue
                if ct == "text/html" and html_body is None:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        html_body = payload.decode(charset, errors="replace")
                elif ct == "text/plain" and plain_body is None:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        plain_body = payload.decode(charset, errors="replace")
        else:
            payload = emailObject.get_payload(decode=True)
            if isinstance(payload, bytes):
                charset = emailObject.get_content_charset() or "utf-8"
                payload = payload.decode(charset, errors="replace")
            if emailObject.get_content_type() == "text/html":
                html_body = payload
            else:
                plain_body = payload

        if html_body is not None:
            self.uiContentWidget.contentWebEngineView.setHtml(unescape(html_body))
        elif plain_body is not None:
            self.uiContentWidget.contentWebEngineView.setHtml(
                f"<pre>{html.escape(plain_body)}</pre>"
            )

        self.uiContentWidget.attachmentListWidget.clear()
        for name in attachments:
            self.uiContentWidget.attachmentListWidget.addItem(QListWidgetItem(name))

