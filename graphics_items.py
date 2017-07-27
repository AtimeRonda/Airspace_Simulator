import Aircraft
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import Qt
import time, math

#Drawing properties
AIRCRAFT_COLOR = "blue"
AIRCRAFT_COLOR_SELECTED = "lightblue"
AIRCRAFT_COLOR_CONFLICT = "red"
AIRCRAFT_BORDER_WIDTH = 1
AIRCRAFT_RADIUS = 1
ROUTE_COLOR = "yellow"
ROUTE_WIDTH = 0.1


class XY(object):
    """Meters coordinates on the airport, with attributes x, y: int"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0.x}, {0.y})".format(self)

    def __sub__(self, other):
        return XY(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)

    def __rmul__(self, k):
        return XY(k * self.x, k * self.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

class Plot(QGraphicsEllipseItem):
    """The view of an aircraft in the GraphicsScene"""

    def __init__(self, moving, f):
        """Plot constructor, creates the ellipse and adds to the scene"""
        super(Plot, self).__init__(None)

        # instance variables
        self.moving = moving
        self.flight = f

        #draw method
        self.pen = QPen()
        self.brush = QBrush()

        self.setRect(0,0,AIRCRAFT_RADIUS, AIRCRAFT_RADIUS)


    def update_position(self, is_conflict):

        #retreiving flight position
        xy = self.flight.getPosition(self.moving.radarView.time)

        x_center = self.moving.radarView.x_center
        y_center = self.moving.radarView.y_center

        distance = math.sqrt(math.pow(x_center-xy.x, 2) + math.pow(y_center-xy.y, 2))
        #print("Point: {} Centre: ({},{}) Distance: {} Radius: {}".format(xy, x_center, y_center, distance, self.moving.radarView.radius // 2))

        if (distance < self.moving.radarView.radius // 2):
            if self.flight.selected:


                #print route
                route = self.flight.route
                l = len(route)
                for i in range(l-1):
                    pen_route = QPen(QColor(ROUTE_COLOR), ROUTE_WIDTH)
                    line = QtWidgets.QGraphicsLineItem(route[i].x, route[i].y, route[i+1].x, route[i+1].y)
                    line.setPen(pen_route)
                    self.moving.radarView.scene.addItem(line)

                self.pen = QPen(QColor(AIRCRAFT_COLOR_SELECTED), AIRCRAFT_BORDER_WIDTH)
                self.brush = QBrush(QColor(AIRCRAFT_COLOR_SELECTED))

            else:
                self.pen = QPen(QColor(AIRCRAFT_COLOR), AIRCRAFT_BORDER_WIDTH)
                self.brush = QBrush(QColor(AIRCRAFT_COLOR))

            if is_conflict:
                self.pen = QPen(QColor(AIRCRAFT_COLOR_CONFLICT), AIRCRAFT_BORDER_WIDTH)
                self.brush = QBrush(QColor(AIRCRAFT_COLOR_CONFLICT))
        else:
            self.pen = QPen(Qt.transparent, AIRCRAFT_BORDER_WIDTH)
            self.brush = QBrush(Qt.transparent)

        self.setPen(self.pen)
        self.setBrush(self.brush)

        #moving point to position
        self.setPos(xy.x, xy.y)

    def mousePressEvent(self, event):
        """stub for interaction on the scene"""
        event.accept()
        current_flights = self.moving.current_flights

        for f in current_flights:
            f.selected = False

        self.moving.radarView.displayFlightId(self.flight)
        self.flight.selected = True

class MovingPlots:

    def __init__(self, radarView, traffic_data):
        self.radarView = radarView
        self.traffic = traffic_data

        self.current_flights = Aircraft.select(traffic_data, radarView.time)

        # find conflicts
        conf, match = Aircraft.detect_in(self.current_flights, self.radarView.time // 1000, self.radarView.time // 1000 + Aircraft.FORECAST)

        self.plot_dict = {}

        # create a plot for each flight
        for flight in self.current_flights:
            plot = Plot(self, flight)  # create a plot
            self.radarView.scene.addItem(plot)  # add it to scene
            self.plot_dict[flight] = plot  # add it to plot dict
            plot.update_position(flight in conf) #argument is is_conflict **** to complete

    def update_plots(self):
        """ updates Plots views """

        new_flights = Aircraft.select(self.traffic, self.radarView.time)

        # add new plots for aircraft who joined
        for f in set(new_flights) - set(self.current_flights):
            plot = Plot(self, f)  # create a plot
            self.radarView.scene.addItem(plot)  # add it to scene
            self.plot_dict[f] = plot  # add it to plot dict

        # remove plots for aircraft who left
        for f in set(self.current_flights) - set(new_flights):
            item = self.plot_dict.pop(f)
            self.radarView.scene.removeItem(item)


        # update all positions
        self.current_flights = new_flights
        conf, match = Aircraft.detect_in(self.current_flights, self.radarView.time // 1000, self.radarView.time // 1000 + Aircraft.FORECAST)

        # finish previous conflict resolutions
        for f in new_flights:
            if (self.radarView.time // 1000 >= f.end_conflict):
                f.correcting = False
                f.end_conflict = 0


        # initiate conflict solver

        for couple in match:
            f1 = couple[0]
            f2 = couple[1]

            #print(f1.correcting, f2.correcting)
            if (f1.correcting == False and f2.correcting == False):
                print("Calling resolve")
                Aircraft.resolve(f1, f2, self.radarView.time)


        for ident in self.plot_dict:
            plot = self.plot_dict[ident]
            plot.update_position(self.plot_dict[ident].flight in conf)