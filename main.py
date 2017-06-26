import sys

import Aircraft
from PyQt5 import QtWidgets

import Airspace as Airspace

if __name__=="__main__":


    #************** Load Data *****************#

    #Setting up some flights
    flight = Aircraft.Flight("AC847", 260, 0)
    print(flight)

    #************** Setting up the app ****************#

    #Initialize Qt Application
    app = QtWidgets.QApplication([])

    #Initialize the radar view
    the_radarview = Airspace.RadarView("Calgary", flight, 1)

    #Setting up the main interface
    win = QtWidgets.QMainWindow()
    win.setCentralWidget(the_radarview)
    win.setWindowTitle("Airspace Simulator")



    #Entering the main loop
    win.showMaximized()
    result = app.exec_()

    #Shutdown
    sys.exit(result)

