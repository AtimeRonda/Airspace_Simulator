# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)

        MainWindow.setMinimumSize(QtCore.QSize(600, 250))
        MainWindow.setWindowIcon(QtGui.QIcon("Interface/ATC_Conflict_Simulator/Unclebob-Spanish-Travel-Plane.ico"))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setIconSize(QtCore.QSize(32, 32))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("Interface")

        self.horizontalGeneralLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalGeneralLayout.setObjectName("horizontalGeneralLayout")

        self.verticalViewLayout = QtWidgets.QVBoxLayout()
        self.verticalViewLayout.setObjectName("verticalViewLayout")
        self.horizontalGeneralLayout.addLayout(self.verticalViewLayout)



        self.line_separator = QtWidgets.QFrame(self.horizontalGeneralLayout)
        self.line_separator.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_separator.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_separator.setLineWidth(1)
        self.line_separator.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_separator.setObjectName("line")





        self.verticalFormLayout = QtWidgets.QVBoxLayout(self.horizontalGeneralLayout)
        self.verticalFormLayout.setObjectName("verticalFormLayout")

        self.spinBox = QtWidgets.QSpinBox(self.verticalFormLayout)
        self.spinBox.setEnabled(True)

        self.spinBox.setMinimumSize(QtCore.QSize(118, 0))
        self.spinBox.setMaximumSize(QtCore.QSize(15000000, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.spinBox.setAutoFillBackground(False)
        self.spinBox.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.spinBox.setObjectName("spinBox")


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ATC Conflict Simulator"))

