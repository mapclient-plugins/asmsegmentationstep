# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(494, 256)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configGroupBox = QGroupBox(Dialog)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.formLayout = QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.idLabel = QLabel(self.configGroupBox)
        self.idLabel.setObjectName(u"idLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.idLabel)

        self.idLineEdit = QLineEdit(self.configGroupBox)
        self.idLineEdit.setObjectName(u"idLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.idLineEdit)

        self.configLabel = QLabel(self.configGroupBox)
        self.configLabel.setObjectName(u"configLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.configLabel)

        self.guiLabel = QLabel(self.configGroupBox)
        self.guiLabel.setObjectName(u"guiLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.guiLabel)

        self.guiCheckBox = QCheckBox(self.configGroupBox)
        self.guiCheckBox.setObjectName(u"guiCheckBox")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.guiCheckBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.configLineEdit = QLineEdit(self.configGroupBox)
        self.configLineEdit.setObjectName(u"configLineEdit")

        self.horizontalLayout.addWidget(self.configLineEdit)

        self.configButton = QPushButton(self.configGroupBox)
        self.configButton.setObjectName(u"configButton")

        self.horizontalLayout.addWidget(self.configButton)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.ppcLabel = QLabel(self.configGroupBox)
        self.ppcLabel.setObjectName(u"ppcLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.ppcLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ppcLineEdit = QLineEdit(self.configGroupBox)
        self.ppcLineEdit.setObjectName(u"ppcLineEdit")

        self.horizontalLayout_2.addWidget(self.ppcLineEdit)

        self.ppcButton = QPushButton(self.configGroupBox)
        self.ppcButton.setObjectName(u"ppcButton")

        self.horizontalLayout_2.addWidget(self.ppcButton)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.idLineEdit, self.configLineEdit)
        QWidget.setTabOrder(self.configLineEdit, self.configButton)
        QWidget.setTabOrder(self.configButton, self.ppcLineEdit)
        QWidget.setTabOrder(self.ppcLineEdit, self.ppcButton)
        QWidget.setTabOrder(self.ppcButton, self.guiCheckBox)
        QWidget.setTabOrder(self.guiCheckBox, self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configure ASM Segmentation Step", None))
        self.configGroupBox.setTitle("")
        self.idLabel.setText(QCoreApplication.translate("Dialog", u"Identifier:  ", None))
        self.configLabel.setText(QCoreApplication.translate("Dialog", u"ASM Config File:", None))
        self.guiLabel.setText(QCoreApplication.translate("Dialog", u"GUI:  ", None))
        self.guiCheckBox.setText("")
        self.configButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.ppcLabel.setText(QCoreApplication.translate("Dialog", u"Texture PC File:", None))
        self.ppcButton.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi

