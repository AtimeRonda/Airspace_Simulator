from PyQt5 import QtWidgets, QtCore
import sys
import Sources.Aircraft as aircraft
import Interface.ATC_Conflict_Simulator.interface as interface


if __name__=="__main__":

    #Initialize Qt Application
    app = QtWidgets.QApplication([])

    #Setting up the main interface
    win = QtWidgets.QMainWindow()
    ui = interface.Ui_MainWindow()
    ui.setupUi(win)
    win.showMaximized()

    #Entering the main loop
    result = app.exec_()

    #Shutdown
    sys.exit(result)

