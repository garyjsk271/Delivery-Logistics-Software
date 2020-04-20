from ExpandableHashMap import *
from provided import *

# Generates two GeoCoord objects from a string of four doubles separated by spaces, 
#   terminated with \n.
# @param geoCoordString The string containing two latitude, longitude pairs 
#   (separated by spaces, terminated with \n).
# @return A tuple of two GeoCoord objects.
def getGeoCoords(geoCoordString):
    coordinates = geoCoordString.split(' ')
    gc1 = GeoCoord(coordinates[0], coordinates[1])
    gc2 = GeoCoord(coordinates[2], coordinates[3][:-1])
    return gc1, gc2
            
# Checks if the element is already contained in a list, and inserts it if it is not.
# @param list The list whose contents will be checked to see if the element 
#   of interest is unique.
# @param element The element to see if it is already contained in the list.
def insertIfUnique(list, element):
    for item in list:
        if item == element:
            return
    list.append(element)

class StreetMap:

    def __init__(self):
        self.__segmentMap  = ExpandableHashMap()

    # Generates a segment map from a given text file containing map data
    # @param mapFile A string of the text file name containing the map data.
    # @raises An exception if the file does not exist.
    def load(self, mapFile):
        mapdata = open(mapFile, "r")
        name      = None
        nSegments = None
        line      = mapdata.readline()
        while line:
            if not name:
                name = line[:-1]
            elif not nSegments:
                nSegments = int(line)
            else:
                for _ in range(nSegments):
                    gc1, gc2  = getGeoCoords(line)
                    streetseg = StreetSegment(gc1, gc2, name)                  
                    if  self.__segmentMap.find(gc1) is None:
                        self.__segmentMap[gc1] = []
                    if  self.__segmentMap.find(gc2) is None:
                        self.__segmentMap[gc2] = []
                    self.__segmentMap[gc1].append(streetseg)
                    self.__segmentMap[gc2].append(streetseg.reversed())
                    line = mapdata.readline()
                name      = None       
                nSegments = None
                continue
            line = mapdata.readline()
        mapdata.close()     

    # Populates a list with all street segments that start with a given geospatial coordinate.
    # @param geoCoord The coordinate we intend to find all street segment connections with.
    # @param segments The list which will be populated with connected segments (if any).
    # @post The 'segments' list will be cleared and populated with all connections (if any).
    #   Contents of 'segments' will be unchanged if no connections exist.
    def getSegmentsThatStartWith(self, geoCoord, segments):
        connections = self.__segmentMap[geoCoord]
        if connections is not None:
            segments.clear()
            segments += connections.copy()