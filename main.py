import sys

import Aircraft
import random
from PyQt5 import QtWidgets

import Airspace as Airspace

NUMBER_AIRCRAFT = 30
CALLSIGNS = ["AC","AF","BA","LH", "QTR","AA"]


if __name__=="__main__":


    #************** Load Data *****************#

    # #Setting up some flights
    # flight = Aircraft.Flight("AC847", 90, 500, 0, 20, 40)
    # flight.straightTrajectory(30)
    # flight.turningTrajectory(160, 10)
    # flight.straightTrajectory(30)
    # flight.turningTrajectory(90, 10)
    # flight.straightTrajectory(120)
    #
    # flight2 = Aircraft.Flight("AF485", 270, 500, 0, 50, 40)
    # flight2.straightTrajectory(200)
    # # flight3 = Aircraft.Flight("LH223", 100, 500, 15)
    # # flight3.straightTrajectory(20, 60, 300)
    #
    #
    # print(flight.route)
    # #flight.straightTrajectory(50)
    #
    # #Loading traffic
    # traffic = Aircraft.Traffic()
    #
    # traffic.load(flight)
    # traffic.load(flight2)
    # # traffic.load(flight3)


    #Generate traffic

    traffic = Aircraft.Traffic()

    for i in range(NUMBER_AIRCRAFT):
        #Making name
        callsign = CALLSIGNS[random.randint(0, len(CALLSIGNS)-1)]
        flight_number = random.randint(0,999)
        callsign = "{}{}".format(callsign, flight_number)

        #Generating basic parameters
        heading = random.randint(0,360)
        speed = random.randint(350, 550)
        x = random.randint(20,60)
        y = random.randint(20,60)
        start_t = random.randint(0,120)

        #Instancing flight
        flight = Aircraft.Flight(callsign, heading, speed, start_t, x, y)



        #Defining a trajectory

        flight_phases = random.randint(3, 10)

        for j in range(flight_phases):
            #straight_or_turn = random.randint(0,2)

            #straight decision
            #if straight_or_turn == 0:
                length = random.randint(20, 100)
                flight.straightTrajectory(length)
            #turn decision
            # elif straight_or_turn == 1:
            #     length = random.randint(20, 100)
            #     deviation = random.randint(-60, 60)
            #     new_heading = flight.heading + deviation
            #     flight.turningTrajectory(new_heading, length)

        #Loading flight
        traffic.load(flight)









    #************** Setting up the app ****************#

    #Initialize Qt Application
    app = QtWidgets.QApplication([])


    #Initialize the radar view
    the_radarview = Airspace.RadarView("Calgary", traffic.flights, 0)

    #Setting up the main interface
    win = QtWidgets.QMainWindow()
    win.setCentralWidget(the_radarview)
    win.setWindowTitle("Airspace Simulator")



    #Entering the main loop
    win.showMaximized()
    result = app.exec_()

    #Shutdown
    sys.exit(result)

