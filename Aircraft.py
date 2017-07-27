import graphics_items as Items
import math

#Constants
STEP = 1 #in seconds
SEP = 5 #traffic separation in NM
FORECAST = 60 # time of conflict detection forecasting in sec


class Flight(object):

    #Constructor
    def __init__(self, callsign, heading, speed, start_t, x_start, y_start):
        self.callsign = callsign
        self.heading = heading
        self.speed = speed
        self.start_t = start_t
        self.start_p = Items.XY(x_start, y_start)
        self.route = [self.start_p]
        self.selected = False
        self.conflicting = False
        self.correcting = False
        self.end_conflict = 0

    def __repr__(self):
        return "Flight {} Heading {} at Speed {}".format(self.callsign, self.heading, self.speed)

    def setSpeed(self,s):
        self.speed = s

    def setHeading(self,h):
        self.heading = h

    def setPositionVector(self, list_of_tuples):
        i=0
        for p in list_of_tuples:
            xy = Items.XY(p[0],p[1])
            self.route.append(xy)
            #print(xy)
        return 0

    def getPosition(self, t):
        """t must be in milliseconds !!!"""
        t = getTimeInSeconds(t)
        return(self.route[t - self.start_t])

    def end_t(self):
        """Flight.end_t() return int: end time step"""
        return self.start_t + len(self.route)

    def distance(self, point_XY, t):
        pos = self.getPosition(t)
        return math.sqrt(pow(point_XY.x-pos.x, 2) + pow(point_XY.y - pos.y, 2))

    #trajectories

    def straightTrajectory(self, nb_points):
        """Define a straight trajectory from the define start point at the heading"""
        l = len(self.route)

        for i in range(nb_points):
            x_next = self.route[l-1].x + math.cos(math.radians(90 - self.heading)) * (self.speed / 3600)
            y_next = self.route[l-1].y + math.sin(math.radians(90 - self.heading)) * (self.speed / 3600)
            self.route.append(Items.XY(x_next, y_next))
            l+=1

    def turningTrajectory(self, new_heading, time_deadline):
        """Add a turn to the current route considering the new heading and deadline target. The function stops computing the trajectory when the new heading is achieved"""
        #The turn must be achieved within the time deadline which is in seconds
        #Next version: check max turn rate
        old_heading = self.heading
        turn_rate = (new_heading - old_heading ) / time_deadline

        for i in range(time_deadline):
            self.heading = self.heading + turn_rate
            self.straightTrajectory(1)
        return 0




class Traffic(object):
    """Encapsulate the traffic data"""

    def __init__(self):
        self.flights = []

    def load(self,f):
        """loads the list of flights"""
        print("Loading {} ...".format(f))
        print("Trajectory lenght: {}".format(len(f.route)))
        self.flights.append(f)
        return 0

    def detect_conflict(self):
        """forecast conflict situations"""
        return 0



# Time string conversions

def hms(t):
    """hms(int) return str
    return a formatted string HH:MM:SS for the given time step"""
    s = t * STEP
    return "{:02d}:{:02d}:{:02d}".format(s // 3600000, s // 1000 // 60 % 60, s // 1000 % 60)

def time_step(str_hms):
    """time_step(str) return int
    return the time step corresponding to a formatted string HH:MM:SS"""
    l = str_hms.replace(':', ' ').split() + [0, 0, 0]
    return (int(l[0]) * 3600000 + int(l[1]) * 60000 + int(l[2]) * 1000) // STEP

# Accessing traffic information

def select(flights, t):
    """select(Flight list, int) return Flight list
    return the flights of 'flights' that are moving at time step 't'"""
    t = getTimeInSeconds(t)
    return [f for f in flights if f.start_t <= t < f.start_t + len(f.route)]

def getTimeInSeconds(t):
    return t // 1000

def check(f1, f2, t):
    """Check if flights f1 and f2 are in conflicts at time t"""

    return abs(f1.getPosition(t *1000) - f2.getPosition(t * 1000)) < SEP

def detect(flights, t):
    """detect(Flight list, int) return (Flight -> Flight list) dict
    return the dictionary of the flights that conflicts at time step 't'"""
    conf = {}
    for i in range(1, len(flights)):
        for j in range(i):
            if check(flights[i], flights[j], t):
                conf[flights[i]] = True
                conf[flights[j]] = True
    return conf


def detect_in(flights, t1, t2):
    """"detect_in(Flight list, int, int) return (Flight -> Flight list) dict
    return the dictionary of the flights that conflicts
    between time steps 't1' and 't2'"""
    conf = {}
    match = []
    for i in range(1, len(flights)):
        ti = min(t2, flights[i].end_t())
        for j in range(i):
            for t in range(t1, min(ti, flights[j].end_t())):
                if check(flights[i], flights[j], t):
                    conf[flights[i]] = True
                    conf[flights[j]] = True
                    match.append((flights[i], flights[j]))
                    break
    return (conf,match)

# conflict resolution
def resolve(f1, f2, t):

    print("Beginning resolving of {} and {}".format(f1, f2))
    pos_f1 = f1.getPosition(t) #find the positions of f1 and f2
    pos_f2 = f2.getPosition(t)


    conf_pos_f1 = f1.getPosition(t + FORECAST*1000) #find their distance to the conflict situation
    conf_pos_f2 = f2.getPosition(t + FORECAST*1000)


    dist_to_conflict_f1 = f1.distance(conf_pos_f1, t)
    dist_to_conflict_f2 = f2.distance(conf_pos_f2, t)




    if dist_to_conflict_f1 <= dist_to_conflict_f2:
        dif = pos_f2 - pos_f1
        angle = math.floor(math.degrees(math.tan(dif.y / dif.x)))


        old_heading = f2.heading
        f2.setHeading(angle)

        dist = f2.distance(pos_f1, t)

        speed_conv = f2.speed /3600 #speed in NM/s
        number_of_points = math.floor(dist / speed_conv)
        to_delete = len(f2.route) - (t//1000) - f2.start_t

        print(f2, number_of_points, to_delete, len(f2.route))
        f2.route = f2.route[:(t//1000)]

        f2.straightTrajectory(number_of_points)

        f2.setHeading(old_heading)
        f2.straightTrajectory(to_delete)
        f2.correcting = True
        f2.end_conflict = (t//1000) + number_of_points
    else:
        dif = pos_f1 - pos_f2
        angle = math.floor(math.degrees(math.tan(dif.y / dif.x)))

        old_heading = f1.heading
        f1.setHeading(angle)

        dist = f1.distance(pos_f2, t)

        speed_conv = f1.speed / 3600  # speed in NM/s
        number_of_points = math.floor(dist / speed_conv)
        to_delete = len(f1.route) - (t // 1000) - f1.start_t

        print(f1, number_of_points, to_delete, len(f1.route))
        f1.route = f1.route[:(t // 1000)]

        f1.straightTrajectory(number_of_points)

        f1.setHeading(old_heading)
        f1.straightTrajectory(to_delete)
        f1.correcting = True
        f1.end_conflict = (t//1000) + number_of_points


    return 0