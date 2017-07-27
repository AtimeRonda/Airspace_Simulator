import math

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QWheelEvent

import Aircraft
import graphics_items as Items

# constants
ANIMATION_DELAY = 300     # milliseconds
AIRSPACE_BORDER_COLOR = "green"
AIRSPACE_BORDER_WIDTH = 1
AIRSPACE_BACKGROUND_COLOR = "black"

#temp var
AIRSPACE_RADIUS = 80

class RadarView(QtWidgets.QWidget):
    def __init__(self, airspace, flights, init_time):
        """ create a window with a view and control buttons """
        super(RadarView, self).__init__()

        #Defining attributes
        self.airspace = airspace
        self.flights = flights
        self.time = init_time #time is in milliseconds
        self.incr = 0

        #Initialize the view properties
        self.grview = None
        self.scene = None
        self.entry = None
        self.console = QtWidgets.QLabel()

        #Draw interface
        self.x_center = 0
        self.y_center = 0
        self.radius = AIRSPACE_RADIUS
        self.circle = QtWidgets.QGraphicsEllipseItem()
        self.build_interface()

        #Draw Airspace zone
        self.draw_airspace()
        self.grview.fitInView(self.grview.sceneRect(), QtCore.Qt.KeepAspectRatio)

        #Create traffic view
        self.moving = Items.MovingPlots(self, flights)

        # initiate a timer to ensure a proper animation
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.advance)
        self.timer.start(ANIMATION_DELAY)

    def build_interface(self):
        # create the root layout of this widget
        hbox_general = QtWidgets.QHBoxLayout(self)
        vbox = QtWidgets.QVBoxLayout()
        vbox_command = QtWidgets.QVBoxLayout()

        hbox_general.addLayout(vbox)
        hbox_general.addLayout(vbox_command)

        # create the view
        self.grview = QtWidgets.QGraphicsView()  # view to navigate in the...
        # ...scene where airport and traffic are displayed
        self.scene = QtWidgets.QGraphicsScene()
        self.grview.setScene(self.scene)  # connect view to scene
        # allow drag and drop of the view
        self.grview.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.grview.setRenderHint(QtGui.QPainter.Antialiasing)
        # allow zooming of the view by mouse scroll (lambda function overrides event handler QGraphicsView.wheelEvent())
        self.grview.wheelEvent = lambda event: self.zoom_view_mouse(event)
        # rotate to invert vertical axis
        self.grview.scale(1, -1)
        vbox.addWidget(self.grview)  # add the view to the layout

        # create layout for time controls and entry
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        # create time controls and entry
        def add_button(text, slot, box):
            """adds a button to the hbox and connects the slot"""
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(slot)
            box.addWidget(button)

        # lambda function allows to pass extra arguments to slots
        # added space around '-' character to avoid different look and feel
        #example: add_button(' - ', lambda: self.zoom_view(0.9))
        emptySlot = pyqtSlot()
        add_button(' - ', lambda: self.zoom_view(1 / 1.1), hbox)
        add_button('+', lambda: self.zoom_view(1.1), hbox)
        hbox.addStretch()
        add_button('<<', lambda: self.forward(-5000), hbox)
        add_button(' <', lambda: self.forward(-1000), hbox)
        add_button('|>', self.playpause, hbox)
        add_button(' >', lambda: self.forward(1000), hbox)
        add_button('>>', lambda: self.forward(5000), hbox)
        self.entry = QtWidgets.QLineEdit()
        hbox.addWidget(self.entry)

        self.entry.setInputMask("00:00:00")
        self.entry.editingFinished.connect(self.change_time)
        self.entry.setText(Aircraft.hms(self.time))
        hbox.addStretch()


        hbox_general.addStretch()

        #create display area
        vbox_command.addWidget(self.console)
        self.console.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        #self.console.setWordWrap(True)
        self.console.setStyleSheet("""
            .QLabel {
                border: 5px solid black;
                background-color: rgb(0, 0, 0);
                color: rgb(11, 216, 52);
                max-height: 40px;
                font: bold 20px;
            }
        """)




        #add_button('Aircraft', emptySlot, vbox_command)
        vbox_command.addStretch()


    def draw_airspace(self):
        """ Adds the airspace to the QGraphicsScene, drawn by the view """
        # Airspace group of graphics items
        airspace_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(airspace_group)

        #Draw the border

        pen = QtGui.QPen(QtGui.QColor(AIRSPACE_BORDER_COLOR), AIRSPACE_BORDER_WIDTH)
        brush = QtGui.QBrush(QtGui.QColor(AIRSPACE_BACKGROUND_COLOR))
        self.circle = QtWidgets.QGraphicsEllipseItem(0, 0, AIRSPACE_RADIUS, AIRSPACE_RADIUS, airspace_group)
        self.circle.setPen(pen)
        self.circle.setBrush(brush)

        #Paint center
        self.x_center = self.circle.rect().width() // 2
        self.y_center = self.circle.rect().height() // 2
        center = QtWidgets.QGraphicsEllipseItem(self.x_center - Items.AIRCRAFT_RADIUS / 20, self.y_center - Items.AIRCRAFT_RADIUS / 20, Items.AIRCRAFT_RADIUS / 10, Items.AIRCRAFT_RADIUS / 10, airspace_group)
        pen = QtGui.QPen(QtGui.QColor("green"), 2)
        brush = QtGui.QBrush(QtGui.QColor("green"))
        center.setPen(pen)
        center.setBrush(brush)


        # #aircraft test
        # aircraft = QtWidgets.QGraphicsEllipseItem(100, 100, 20, 20,circle)
        # pen = QtGui.QPen(QtGui.QColor("yellow"), 2)
        # brush = QtGui.QBrush(QtGui.QColor("yellow"))
        # aircraft.setPen(pen)
        # aircraft.setBrush(brush)


    def update_traffic(self):
        self.moving.update_plots()

    def set_time(self, time):
        """sets the time to the new value, and updates the two views"""
        self.entry.setText(Aircraft.hms(time))
        self.time = time #set time in milliseconds
        self.update_traffic()

    @QtCore.pyqtSlot(int)
    def zoom_view(self, value):
        """this slot updates the zoom factor of the view """
        self.grview.scale(value, value)

    @QtCore.pyqtSlot(QWheelEvent)
    def zoom_view_mouse(self, event):
        """this slot updates the zoom factor of the view when mouse scroll occurs"""
        self.grview.setTransformationAnchor(self.grview.AnchorUnderMouse)
        # factor = 1.1 if 0 < event.angleDelta().y() else 1 / 1.1
        factor = math.pow(1.001, event.angleDelta().y())
        self.grview.scale(factor, factor)

    @QtCore.pyqtSlot()
    def advance(self):
        """this slot computes the new time at each time out"""
        self.set_time(self.time + ANIMATION_DELAY + (self.incr * ANIMATION_DELAY // 1000))
        self.update_traffic()

    @QtCore.pyqtSlot()
    def playpause(self):
        """this slot toggles the replay using the timer as model"""
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(ANIMATION_DELAY)

    @QtCore.pyqtSlot(int)
    def forward(self, i):
        """this slot updates the speed of the replay"""
        self.incr = i

    @QtCore.pyqtSlot()
    def change_time(self):
        """slot triggered when a new time is input in the text field"""
        self.set_time(Aircraft.time_step(self.entry.text()))
        self.update_traffic()

    @QtCore.pyqtSlot()
    def displayFlightId(self, flight):
        text = "Flight {} Heading {} at Speed {}".format(flight.callsign, math.ceil(flight.heading), flight.speed)
        self.console.setText(text)
        return 0