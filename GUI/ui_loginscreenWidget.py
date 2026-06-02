from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loginScreenWidget(object):
    def setupUi(self, loginScreenWidget):
        # Setting up window settings
        loginScreenWidget.setObjectName("loginScreenWidget")
        loginScreenWidget.setFixedSize(440, 380)
        font = QtGui.QFont()
        font.setFamily("Monospace")

        # Creating layout objects
        self.gridLayoutWidget = QtWidgets.QWidget(loginScreenWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 380, 340))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # Provider row
        self.horizontalLayoutProvider = QtWidgets.QHBoxLayout()
        self.horizontalLayoutProvider.setObjectName("horizontalLayoutProvider")
        self.providerLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.providerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.providerLabel.setObjectName("providerLabel")
        self.horizontalLayoutProvider.addWidget(self.providerLabel)
        self.providerComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.providerComboBox.setObjectName("providerComboBox")
        self.horizontalLayoutProvider.addWidget(self.providerComboBox)
        self.horizontalLayoutProvider.setStretch(0, 1)
        self.horizontalLayoutProvider.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutProvider, 0, 0, 1, 1)

        # Email row
        self.horizontalLayoutEmail = QtWidgets.QHBoxLayout()
        self.horizontalLayoutEmail.setObjectName("horizontalLayoutEmail")
        self.emailLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.emailLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.emailLabel.setObjectName("emailLabel")
        self.horizontalLayoutEmail.addWidget(self.emailLabel)
        self.loginLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.loginLineEdit.setObjectName("loginLineEdit")
        self.horizontalLayoutEmail.addWidget(self.loginLineEdit)
        self.horizontalLayoutEmail.setStretch(0, 1)
        self.horizontalLayoutEmail.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutEmail, 1, 0, 1, 1)

        # Password row
        self.horizontalLayoutPassword = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPassword.setObjectName("horizontalLayoutPassword")
        self.passwordLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.passwordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLabel.setObjectName("passwordLabel")
        self.horizontalLayoutPassword.addWidget(self.passwordLabel)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.horizontalLayoutPassword.addWidget(self.passwordLineEdit)
        self.horizontalLayoutPassword.setStretch(0, 1)
        self.horizontalLayoutPassword.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutPassword, 2, 0, 1, 1)

        # IMAP server row
        self.horizontalLayoutImap = QtWidgets.QHBoxLayout()
        self.horizontalLayoutImap.setObjectName("horizontalLayoutImap")
        self.imapLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.imapLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imapLabel.setObjectName("imapLabel")
        self.horizontalLayoutImap.addWidget(self.imapLabel)
        self.imapServerLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.imapServerLineEdit.setObjectName("imapServerLineEdit")
        self.horizontalLayoutImap.addWidget(self.imapServerLineEdit)
        self.imapPortSpinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.imapPortSpinBox.setObjectName("imapPortSpinBox")
        self.imapPortSpinBox.setRange(1, 65535)
        self.imapPortSpinBox.setValue(993)
        self.imapPortSpinBox.setFixedWidth(65)
        self.horizontalLayoutImap.addWidget(self.imapPortSpinBox)
        self.horizontalLayoutImap.setStretch(0, 1)
        self.horizontalLayoutImap.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutImap, 3, 0, 1, 1)

        # SMTP server row
        self.horizontalLayoutSmtp = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSmtp.setObjectName("horizontalLayoutSmtp")
        self.smtpLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.smtpLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.smtpLabel.setObjectName("smtpLabel")
        self.horizontalLayoutSmtp.addWidget(self.smtpLabel)
        self.smtpServerLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.smtpServerLineEdit.setObjectName("smtpServerLineEdit")
        self.horizontalLayoutSmtp.addWidget(self.smtpServerLineEdit)
        self.smtpPortSpinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.smtpPortSpinBox.setObjectName("smtpPortSpinBox")
        self.smtpPortSpinBox.setRange(1, 65535)
        self.smtpPortSpinBox.setValue(465)
        self.smtpPortSpinBox.setFixedWidth(65)
        self.horizontalLayoutSmtp.addWidget(self.smtpPortSpinBox)
        self.horizontalLayoutSmtp.setStretch(0, 1)
        self.horizontalLayoutSmtp.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutSmtp, 4, 0, 1, 1)

        # Remember me checkbox setup
        self.rememberMeCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.rememberMeCheckBox.setObjectName("rememberMeCheckBox")
        self.gridLayout.addWidget(self.rememberMeCheckBox, 5, 0, 1, 1)

        # Buttons row
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        self.loginButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayoutButtons.addWidget(self.loginButton)
        self.exitButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayoutButtons.addWidget(self.exitButton)
        self.gridLayout.addLayout(self.horizontalLayoutButtons, 6, 0, 1, 1)

        self.retranslateUi(loginScreenWidget)
        QtCore.QMetaObject.connectSlotsByName(loginScreenWidget)

    def retranslateUi(self, loginScreenWidget):
        """Method translation into other languages"""

        _translate = QtCore.QCoreApplication.translate
        loginScreenWidget.setWindowTitle(_translate("loginScreenWidget", "Login"))
        self.loginButton.setText(_translate("loginScreenWidget", "Login"))
        self.exitButton.setText(_translate("loginScreenWidget", "Exit"))
        self.rememberMeCheckBox.setText(
            _translate("loginScreenWidget", "Remember password")
        )
        self.passwordLabel.setText(_translate("loginScreenWidget", "Password"))
        self.emailLabel.setText(_translate("loginScreenWidget", "Email"))
        self.providerLabel.setText(_translate("loginScreenWidget", "Provider"))
        self.imapLabel.setText(_translate("loginScreenWidget", "IMAP"))
        self.smtpLabel.setText(_translate("loginScreenWidget", "SMTP"))

