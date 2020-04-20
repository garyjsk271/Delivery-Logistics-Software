from ExpandableHashMap import *
from heapq import *
from provided import *

class PointToPointRouter:
    # the streetmap argument must contain loaded map data.
    def __init__(self, streetmap):
        self.__map = streetmap

    # Generates a route from the starting coordinate to the ending coordinate.
    # @param start The starting geospatial coordinate.
    # @param end The ending geospatial coordinate location.
    # @param route A list of connected street segments forming the route.
    # @return A tuple of the delivery result and distance of the route.
    #  *If either geospatial coordinate is bad, will return (BAD_COORD, -1)
    # @post If there exists a path between the start and end geospatial coordinate,
    #  the current contents of 'route' will be cleared and populated with the new route.
    def generatePointToPointRoute(self, start, end, route):

        connectionsWithStart = []
        connectionsWithEnd   = []
        self.__map.getSegmentsThatStartWith(start, connectionsWithStart)
        self.__map.getSegmentsThatStartWith(end, connectionsWithEnd)

        if len(connectionsWithStart) == 0 or len(connectionsWithEnd) == 0:
            return DeliveryResult.BAD_COORD, -1
        elif start == end:
            route.clear()
            return DeliveryResult.DELIVERY_SUCCESS, 0

        dist = ExpandableHashMap()
        dist[start] = 0

        prev = ExpandableHashMap()
        prev[start] = None

        # maintain a priority queue of elements (distance, StreetSegment)
        pq = []        
        heappush(pq, (0, StreetSegment(None, start, '')) )

        while len(pq) > 0:
            distance, street = heappop(pq)
            u = street.end

            if (dist[u] != distance):
                continue
            
            if prev[end] is not None:
                route.clear()
                street = prev[end]
                while street is not None:
                    route[:0] = [street]
                    street = prev[street.start]
                return DeliveryResult.DELIVERY_SUCCESS, dist[end]
                    
            neighbors = []
            self.__map.getSegmentsThatStartWith(u, neighbors)
            for neighbor in neighbors:
                v = neighbor.end
                if dist[u] is None:
                    dist[u] = float('inf')
                if dist[v] is None:
                    dist[v] = float('inf')

                tentative_dist = dist[u] + distanceEarthMiles(u, v)
                
                if tentative_dist < dist[v]:
                    dist[v] = tentative_dist
                    prev[v] = neighbor
                    heappush(pq, [tentative_dist, neighbor])

        return DeliveryResult.NO_ROUTE, -1
