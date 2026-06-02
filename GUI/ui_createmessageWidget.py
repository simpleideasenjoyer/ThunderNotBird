# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateMessageWidget(object):
    def setupUi(self, CreateMessageWidget):
        CreateMessageWidget.setObjectName("CreateMessageWidget")
        CreateMessageWidget.resize(823, 650)
        CreateMessageWidget.setBaseSize(QtCore.QSize(823, 650))
        self.verticalLayoutWidget = QtWidgets.QWidget(CreateMessageWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 19, 811, 621))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # To row
        self.horizontalLayout_to = QtWidgets.QHBoxLayout()
        self.horizontalLayout_to.setObjectName("horizontalLayout_to")
        self.toLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.toLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.toLabel.setObjectName("toLabel")
        self.horizontalLayout_to.addWidget(self.toLabel)
        self.toLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.toLineEdit.setObjectName("toLineEdit")
        self.horizontalLayout_to.addWidget(self.toLineEdit)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.horizontalLayout_to.addItem(spacerItem)
        self.sendButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout_to.addWidget(self.sendButton)
        self.horizontalLayout_to.setStretch(0, 1)
        self.horizontalLayout_to.setStretch(1, 9)
        self.horizontalLayout_to.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_to)

        # CC row
        self.horizontalLayout_cc = QtWidgets.QHBoxLayout()
        self.horizontalLayout_cc.setObjectName("horizontalLayout_cc")
        self.ccLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ccLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ccLabel.setObjectName("ccLabel")
        self.horizontalLayout_cc.addWidget(self.ccLabel)
        self.ccLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ccLineEdit.setObjectName("ccLineEdit")
        self.horizontalLayout_cc.addWidget(self.ccLineEdit)
        self.horizontalLayout_cc.setStretch(0, 1)
        self.horizontalLayout_cc.setStretch(1, 10)
        self.verticalLayout.addLayout(self.horizontalLayout_cc)

        # BCC row
        self.horizontalLayout_bcc = QtWidgets.QHBoxLayout()
        self.horizontalLayout_bcc.setObjectName("horizontalLayout_bcc")
        self.bccLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bccLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.bccLabel.setObjectName("bccLabel")
        self.horizontalLayout_bcc.addWidget(self.bccLabel)
        self.bccLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.bccLineEdit.setObjectName("bccLineEdit")
        self.horizontalLayout_bcc.addWidget(self.bccLineEdit)
        self.horizontalLayout_bcc.setStretch(0, 1)
        self.horizontalLayout_bcc.setStretch(1, 10)
        self.verticalLayout.addLayout(self.horizontalLayout_bcc)

        # Subject row
        self.horizontalLayout_subject = QtWidgets.QHBoxLayout()
        self.horizontalLayout_subject.setObjectName("horizontalLayout_subject")
        self.subjectLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.subjectLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.subjectLabel.setObjectName("subjectLabel")
        self.horizontalLayout_subject.addWidget(self.subjectLabel)
        self.subjectLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.subjectLineEdit.setObjectName("subjectLineEdit")
        self.horizontalLayout_subject.addWidget(self.subjectLineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.horizontalLayout_subject.addItem(spacerItem1)
        self.addAttachmentButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addAttachmentButton.setObjectName("addAttachmentButton")
        self.horizontalLayout_subject.addWidget(self.addAttachmentButton)
        self.horizontalLayout_subject.setStretch(0, 1)
        self.horizontalLayout_subject.setStretch(1, 10)
        self.horizontalLayout_subject.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_subject)

        self.messageBoxTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.messageBoxTextEdit.setObjectName("messageBoxTextEdit")
        self.verticalLayout.addWidget(self.messageBoxTextEdit)
        self.attachmentListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.attachmentListWidget.setObjectName("attachmentListWidget")
        self.verticalLayout.addWidget(self.attachmentListWidget)
        self.verticalLayout.setStretch(4, 9)
        self.verticalLayout.setStretch(5, 1)

        self.retranslateUi(CreateMessageWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateMessageWidget)

    def retranslateUi(self, CreateMessageWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateMessageWidget.setWindowTitle(
            _translate("CreateMessageWidget", "Create Message")
        )
        self.toLabel.setText(_translate("CreateMessageWidget", "To:"))
        self.sendButton.setText(_translate("CreateMessageWidget", "Send"))
        self.ccLabel.setText(_translate("CreateMessageWidget", "CC:"))
        self.bccLabel.setText(_translate("CreateMessageWidget", "BCC:"))
        self.subjectLabel.setText(_translate("CreateMessageWidget", "Subject:"))
        self.addAttachmentButton.setText(_translate("CreateMessageWidget", "Add"))

