# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/configuredialog.ui'
#
# Created: Mon Jun  1 10:53:16 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(494, 256)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.configGroupBox = QtGui.QGroupBox(Dialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.idLabel = QtGui.QLabel(self.configGroupBox)
        self.idLabel.setObjectName("idLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.idLabel)
        self.idLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.idLineEdit.setObjectName("idLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.idLineEdit)
        self.configLabel = QtGui.QLabel(self.configGroupBox)
        self.configLabel.setObjectName("configLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.configLabel)
        self.guiLabel = QtGui.QLabel(self.configGroupBox)
        self.guiLabel.setObjectName("guiLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.guiLabel)
        self.guiCheckBox = QtGui.QCheckBox(self.configGroupBox)
        self.guiCheckBox.setText("")
        self.guiCheckBox.setObjectName("guiCheckBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.guiCheckBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.configLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.configLineEdit.setObjectName("configLineEdit")
        self.horizontalLayout.addWidget(self.configLineEdit)
        self.configButton = QtGui.QPushButton(self.configGroupBox)
        self.configButton.setObjectName("configButton")
        self.horizontalLayout.addWidget(self.configButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.ppcLabel = QtGui.QLabel(self.configGroupBox)
        self.ppcLabel.setObjectName("ppcLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.ppcLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ppcLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.ppcLineEdit.setObjectName("ppcLineEdit")
        self.horizontalLayout_2.addWidget(self.ppcLineEdit)
        self.ppcButton = QtGui.QPushButton(self.configGroupBox)
        self.ppcButton.setObjectName("ppcButton")
        self.horizontalLayout_2.addWidget(self.ppcButton)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.idLineEdit, self.configLineEdit)
        Dialog.setTabOrder(self.configLineEdit, self.configButton)
        Dialog.setTabOrder(self.configButton, self.ppcLineEdit)
        Dialog.setTabOrder(self.ppcLineEdit, self.ppcButton)
        Dialog.setTabOrder(self.ppcButton, self.guiCheckBox)
        Dialog.setTabOrder(self.guiCheckBox, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Configure ASM Segmentation Step", None, QtGui.QApplication.UnicodeUTF8))
        self.idLabel.setText(QtGui.QApplication.translate("Dialog", "Identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.configLabel.setText(QtGui.QApplication.translate("Dialog", "ASM Config File:", None, QtGui.QApplication.UnicodeUTF8))
        self.guiLabel.setText(QtGui.QApplication.translate("Dialog", "GUI:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.configButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.ppcLabel.setText(QtGui.QApplication.translate("Dialog", "Texture PC File:", None, QtGui.QApplication.UnicodeUTF8))
        self.ppcButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))

