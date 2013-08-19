# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_splitmultipart.ui'
#
# Created: Tue Aug  6 20:39:48 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SplitMultipart(object):
    def setupUi(self, SplitMultipart):
        SplitMultipart.setObjectName(_fromUtf8("SplitMultipart"))
        SplitMultipart.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(SplitMultipart)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(SplitMultipart)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SplitMultipart.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SplitMultipart.reject)
        QtCore.QMetaObject.connectSlotsByName(SplitMultipart)

    def retranslateUi(self, SplitMultipart):
        SplitMultipart.setWindowTitle(QtGui.QApplication.translate("SplitMultipart", "SplitMultipart", None, QtGui.QApplication.UnicodeUTF8))

