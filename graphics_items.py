import Aircraft
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem

#Drawing properties
AIRCRAFT_COLOR = "blue"
AIRCRAFT_BORDER_WIDTH = 1
AIRCRAFT_RADIUS = 3


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

    def __init__(self, f):
        """Plot constructor, creates the ellipse and adds to the scene"""
        super(Plot, self).__init__(None)

        # instance variables
        self.flight = f

        def update_position(self, t):

            #configuring output display
            pen = QPen(QColor(AIRCRAFT_COLOR), AIRCRAFT_COLOR)
            brush = QBrush(QColor(AIRCRAFT_COLOR))
            self.setPen(pen)
            self.setBrush(brush)

            #retreiving flight position
            xy = f.getPosition(t)
            self.setPosition(xy.x, xy.y)

class MovingPlots:

    def __init__(self, radarView, traffic):
        self.radarView = radarView
        self.traffic = traffic

        self.current_flights = Aircraft.select(traffic.flights, radarView.time)

        self.plot_dict = {}
        # create a plot for each flight
        for flight in self.current_flights:
            plot = Plot(self, flight)  # create a plot
            self.radarView.scene.addItem(plot)  # add it to scene
            self.plot_dict[flight] = plot  # add it to plot dict
            plot.update_position(flight)
