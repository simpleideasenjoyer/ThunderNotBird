from PyQt5 import QtCore, QtGui, QtWidgets
import imaplib
import sys


class Ui_loginScreenWidget(object):
    def setupUi(self, loginScreenWidget):
        # Setting up window settings
        loginScreenWidget.setObjectName("loginScreenWidget")
        loginScreenWidget.setFixedSize(400, 300)
        font = QtGui.QFont()
        font.setFamily("Monospace")

        # Creating layout objects
        self.gridLayoutWidget = QtWidgets.QWidget(loginScreenWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 20, 311, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        self.horizontalLayoutPassword = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPassword.setObjectName("horizontalLayoutPassword")
        self.horizontalLayoutEmail = QtWidgets.QHBoxLayout()
        self.horizontalLayoutEmail.setObjectName("horizontalLayoutEmail")

        # Login button setup
        self.loginButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayoutButtons.addWidget(self.loginButton)

        # Exit button setup
        self.exitButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayoutButtons.addWidget(self.exitButton)
        self.gridLayout.addLayout(self.horizontalLayoutButtons, 4, 0, 1, 1)

        # Remember me checkbox setup
        self.rememberMeCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.rememberMeCheckBox.setObjectName("rememberMeCheckBox")
        self.gridLayout.addWidget(self.rememberMeCheckBox, 3, 0, 1, 1)

        # Password label setup
        self.passwordLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.passwordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLabel.setObjectName("passwordLabel")
        self.horizontalLayoutPassword.addWidget(self.passwordLabel)

        # Password line edit setup
        self.passwordLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.horizontalLayoutPassword.addWidget(self.passwordLineEdit)
        self.horizontalLayoutPassword.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutPassword, 1, 0, 1, 1)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Email label setup
        self.emailLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.emailLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.emailLabel.setObjectName("emailLabel")
        self.horizontalLayoutEmail.addWidget(self.emailLabel)

        # Login line edit setup
        self.loginLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.loginLineEdit.setObjectName("loginLineEdit")
        self.horizontalLayoutEmail.addWidget(self.loginLineEdit)
        self.horizontalLayoutEmail.setStretch(0, 1)
        self.horizontalLayoutEmail.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayoutEmail, 0, 0, 1, 1)

        # Info Label
        self.infoLabel = QtWidgets.QLabel()
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayoutPassword.addWidget(self.infoLabel)

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
