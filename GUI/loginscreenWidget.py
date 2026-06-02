from PyQt5.QtWidgets import QWidget, QMessageBox
from .ui_loginscreenWidget import Ui_loginScreenWidget
from PyQt5.QtCore import pyqtSignal
import sys
from .utils.logic import ReceiveEmail
from .utils.config import PROVIDERS


class LoginScreenWidget(QWidget, Ui_loginScreenWidget):
    loginSuccessful = pyqtSignal()
    objectTransfer = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.uiLogin = Ui_loginScreenWidget()
        self.uiLogin.setupUi(self)

        # Populate provider combobox
        for provider in PROVIDERS:
            self.uiLogin.providerComboBox.addItem(provider)
        self._apply_provider(self.uiLogin.providerComboBox.currentText())

        self.uiLogin.providerComboBox.currentTextChanged.connect(self._apply_provider)
        self.uiLogin.loginButton.clicked.connect(self.check_login)
        self.uiLogin.exitButton.clicked.connect(self.exit)

    def _apply_provider(self, provider_name: str) -> None:
        """Auto-fill IMAP/SMTP fields based on the selected provider."""
        settings = PROVIDERS.get(provider_name, PROVIDERS["Custom"])
        self.uiLogin.imapServerLineEdit.setText(settings["imap_server"])
        self.uiLogin.imapPortSpinBox.setValue(settings["imap_port"])
        self.uiLogin.smtpServerLineEdit.setText(settings["smtp_server"])
        self.uiLogin.smtpPortSpinBox.setValue(settings["smtp_port"])
        is_custom = provider_name == "Custom"
        self.uiLogin.imapServerLineEdit.setReadOnly(not is_custom)
        self.uiLogin.smtpServerLineEdit.setReadOnly(not is_custom)
        self.uiLogin.imapPortSpinBox.setReadOnly(not is_custom)
        self.uiLogin.smtpPortSpinBox.setReadOnly(not is_custom)

    def check_login(self) -> None:
        email = self.uiLogin.loginLineEdit.text().strip()
        password = self.uiLogin.passwordLineEdit.text()
        imap_server = self.uiLogin.imapServerLineEdit.text().strip()
        imap_port = self.uiLogin.imapPortSpinBox.value()
        smtp_server = self.uiLogin.smtpServerLineEdit.text().strip()
        smtp_port = self.uiLogin.smtpPortSpinBox.value()
        provider = self.uiLogin.providerComboBox.currentText()
        smtp_ssl = PROVIDERS.get(provider, PROVIDERS["Custom"])["smtp_ssl"]

        if not email or not password:
            QMessageBox.warning(self, "Login", "Please enter your email and password.")
            return
        if not imap_server or not smtp_server:
            QMessageBox.warning(self, "Login", "Please enter IMAP and SMTP server addresses.")
            return

        try:
            imapObject = ReceiveEmail(
                email,
                password,
                imapServer=imap_server,
                imapPort=imap_port,
                smtpServer=smtp_server,
                smtpPort=smtp_port,
                smtpSsl=smtp_ssl,
            )
            self.loginSuccessful.emit()
            self.objectTransfer.emit(imapObject)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Login failed", f"Could not connect to mailbox:\n{e}")

    def exit(self) -> None:
        sys.exit()

