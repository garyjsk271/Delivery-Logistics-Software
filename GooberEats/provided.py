from enum import Enum

class DeliveryResult(Enum):
    DELIVERY_SUCCESS = 0
    NO_ROUTE         = 1
    BAD_COORD        = 2

"""
Dataclass could have been used if mutability is desired to emulate a C++ struct.
However, this would result in an undesired side-effect when hashing them.
hash() in Python returns a hashed value only for immutable objects (exception thrown otherwise).
"""
class GeoCoord:
    def __init__(self, latitudeText, longitudeText):
        self.latitudeText  = latitudeText
        self.longitudeText = longitudeText
        self.latitude      = float(latitudeText)
        self.longitude     = float(longitudeText)

    def __eq__(self, other):
        return self.latitudeText == other.latitudeText and\
            self.longitudeText == other.longitudeText
    
    def __lt__(self, other):
        if (self.latitudeText == other.latitudeText):
            return self.longitudeText < other.longitudeText
        return self.latitudeText < other.latitudeText
    
    # Specs provided a utility function that hashes GeoCoords.
    # However, in Python, you can override __hash__ instead,
    # resulting in slightly more organized code.
    def __hash__(self):
        return hash(self.latitudeText + self.longitudeText)

class StreetSegment:
    def __init__(self, start, end, name):
        self.start = start
        self.end   = end
        self.name  = name

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and\
            self.name == other.name
    
    def __lt__(self, other):
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start
        
    def reversed(self):
        return StreetSegment(self.end, self.start, self.name)

class DeliveryRequest():
    def __init__(self, item, location):
        self.item = item
        self.location = location

class CommandType(Enum):
    INVALID = 0
    PROCEED = 1
    TURN    = 2
    DELIVER = 3

class DeliveryCommand:
    def __init__(self):
        self.__streetName = ''
        self.__direction  = ''
        self.__item       = ''
        self.__distance   = 0.0
        self.__type       = CommandType.INVALID
    
    def initAsProceedCommand(self, direction, streetName, dist):
        self.__direction  = direction
        self.__streetName = streetName
        self.__distance   = dist
        self.__type       = CommandType.PROCEED
        
    def initAsTurnCommand(self, direction, streetName):
        self.__direction  = direction
        self.__streetName = streetName
        self.__distance   = 0
        self.__type       = CommandType.TURN
        
    def initAsDeliverCommand(self, item):
        self.__item = item
        self.__type = CommandType.DELIVER
    
    def increaseDistance(self, byThisMuch):
        self.__distance += byThisMuch
        
    def streetName(self):
        return self.__streetName
    
    def description(self):    
        if (self.__type == CommandType.INVALID):
            return '<invalid>'
        elif (self.__type == CommandType.TURN):
            return 'Turn ' + self.__direction + ' on ' + self.__streetName
        elif (self.__type == CommandType.PROCEED):
            return 'Proceed ' + self.__direction + ' on ' + self.__streetName\
                    + ' for ' + str(self.__distance) + ' miles'
        else:
            return 'Deliver ' + self.__item

import math

def deg2rad(deg):
    return math.radians(deg)

def rad2deg(rad):
    return math.degrees(rad)

def distanceEarthKM(g1, g2):
    earthRadiusKM = 6371.0
    lat1r = deg2rad(g1.latitude)
    lon1r = deg2rad(g1.longitude)
    lat2r = deg2rad(g2.latitude)
    lon2r = deg2rad(g2.longitude)
    u = math.sin((lat2r - lat1r) / 2)
    v = math.sin((lon2r - lon1r) / 2)
    return 2.0 * earthRadiusKM * math.asin(\
        math.sqrt(u**2 + math.cos(lat1r) * math.cos(lat2r) * v**2))

def distanceEarthMiles(g1, g2):
    milesPerKm = 1 / 1.609344
    return distanceEarthKM(g1, g2) * milesPerKm

def segmentDistance(streetsegment):
    return distanceEarthMiles(streetsegment.start, streetsegment.end)

def routeDistance(route):
    distance = 0
    for segment in route:
        distance += segmentDistance(segment)
    return distance

def angleBetween2Lines(line1, line2):
    angle1 = math.atan2(line1.end.latitude - line1.start.latitude,\
                        line1.end.longitude - line1.start.longitude)
    angle2 = math.atan2(line2.end.latitude - line2.start.latitude,\
                        line2.end.longitude - line2.start.longitude)
    result = rad2deg(angle2 - angle1)
    if (result < 0):
        result += 360
    return result

def angleOfline(line):
    angle = math.atan2(line.end.latitude - line.start.latitude,\
                       line.end.longitude - line.start.longitude)
    result = rad2deg(angle)
    if (result < 0):
        result += 360
    return result


