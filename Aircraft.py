import graphics_items as items

#Constants
STEP = 1 #in seconds


class Flight(object):

    #Constructor
    def __init__(self, callsign, heading, start_t):
        self.callsign = callsign
        self.heading = heading
        self.speed = 0
        self.start_t = start_t
        self.route = []


    def __repr__(self):
        return "Flight {} Heading {} at Speed {}".format(self.callsign, self.heading, self.speed)

    def setPositionVector(self, list_of_tuples):
        i=0
        while i<len(list_of_tuples):
            self.route.append(items.XY(list_of_tuples[i][0], list_of_tuples[i][1]))
        return 0


class Traffic(object):
    """Encapsulate the traffic data"""

    def __init__(self):
        self.flights = []

    def load(self):
        """loads the list of flights"""
        return 0

    def detect_conflict(self):
        """forecast conflict situations"""
        return 0



# Time string conversions

def hms(t):
    """hms(int) return str
    return a formatted string HH:MM:SS for the given time step"""
    s = t * STEP
    return "{:02d}:{:02d}:{:02d}".format(s // 3600, s // 60 % 60, s % 60)

# Accessing traffic information

def select(flights, t):
    """select(Flight list, int) return Flight list
    return the flights of 'flights' that are moving at time step 't'"""
    return [f for f in flights if f.start_t <= t < f.start_t + len(f.route)]