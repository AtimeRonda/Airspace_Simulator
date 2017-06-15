class Flight(object):

    #Constructor
    def __init__(self, callsign, heading, start_t):
        self.callsign = callsign
        self.heading = heading
        self.speed = 0
        self.start_t = start_t


    def __repr__(self):
        return "Flight {()} Heading {()} at Speed {()}".format(self.callsign, self.heading, self.speed)