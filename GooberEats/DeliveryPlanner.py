from DeliveryOptimizer import DeliveryOptimizer
from PointToPointRouter import PointToPointRouter
from provided import *

# Function which gets the delivery command type.
# @param seg1 The first street segment. 
# @param seg2 The second street segment.
# @return The command type determined by the angle between the two street segments.
def commandType(seg1, seg2):
    angle = angleBetween2Lines(seg1, seg2)
    if angle < 1 or angle > 360:
        return CommandType.PROCEED
    return CommandType.TURN

# Function that gets the direction of a street segment.
# @param streetsegment The street segment whose direction will be determined.
# @return The direction of the proceed command determined by the angle of the street segment.
def proceedDirection(streetsegment):
    direction = ''
    angle = angleOfline(streetsegment)
    if 0 <= angle < 22.5:
        direction = 'east'
    elif 22.5 <= angle < 67.5:
        direction = 'northeast'
    elif 67.5 <= angle < 112.5:
        direction = 'north'
    elif 112.5 <= angle < 157.5:
        direction = 'northwest'
    elif 157.5 <= angle < 202.5:
        direction = 'west'
    elif 202.5 <= angle < 247.5:
        direction = 'southwest'
    elif 247.5 <= angle < 292.5:
        direction = 'south'
    elif 292.5 <= angle < 337.5:
        direction = 'southeast'
    else:
        direction = 'east'
    return direction

# Gets the turn direction between two street segments.
# @param seg1 The first segment.
# @param seg2 The second segment.
# @return The turn direction based on the angle between the two street segments.
# @pre The angle between the two segments must be at least 1 and less than 360.
def turnDirection(seg1, seg2):
    angle = angleBetween2Lines(seg1, seg2)
    return 'left' if 1 <= angle < 180 else 'right'

# Generates a list of appropriate delivery commands of a given route.
# @param route A list of street segments for which the commands is to be generated.
# @param commands A list to be populated with the appropriate delivery commands (in order).
# @param deliveries A list of delivery requests to be fulfilled.
# @post 'commands' will be cleared and populated with the appropriate delivery commands.
def generateDeliveryCommand(route, commands, deliveries):
    commands.clear()
    # Generate first command from depot to first GeoCoord.
    command = DeliveryCommand()
    command.initAsProceedCommand(proceedDirection(route[0]), route[0].name, 
        segmentDistance(route[0]) )
    commands.append(command)

    # Iterate from second street segment to last segment (from last delivery back to depot).
    i = 1   # index of route
    j = 0   # index of deliveries
    while i < len(route):
        if (commands[-1].streetName() == route[i].name):    # Proceed since still on same street.
            commands[-1].increaseDistance(segmentDistance(route[i]) )
        else:   # Turn and/or proceed onto new street.
            command = DeliveryCommand()
            seg1 = route[i-1]
            seg2 = route[i]
            if commandType(seg1, seg2) == CommandType.TURN:
                command.initAsTurnCommand(turnDirection(seg1, seg2), seg2.name)
                commands.append(command)

            command = DeliveryCommand()
            command.initAsProceedCommand(proceedDirection(seg2), seg2.name, 
                segmentDistance(seg2) )
            commands.append(command)
        i += 1 
        # Check if a delivery is to be made.
        if i < len(route) and j < len(deliveries) and route[i].end == deliveries[j].location:
            command = DeliveryCommand()
            command.initAsDeliverCommand(deliveries[j].item)
            commands.append(command)
            i += 1
            j += 1
            
            # Delivery command immediately after delivery shall always be 'proceed'
            command = DeliveryCommand()
            command.initAsProceedCommand(proceedDirection(route[i]), route[i].name, 
                segmentDistance(route[i]) )
            commands.append(command)
            i += 1

class DeliveryPlanner:
    def __init__(self, streetmap):
        self.__router = PointToPointRouter(streetmap)
        self.__optimizer = DeliveryOptimizer(streetmap)
        
    # Generates a delivery plan fulfilling all delivery requests.
    # @param depotLocation The geospatial coordinate of the depot (i.e start & end point)
    # @param deliveries A list of all delivery requests to be fulfilled.
    # @param commands A list of delivery commands to be populated with delivery instructions.
    # @return A tuple of the delivery result and the total distance through the delivery plan.
    def generateDeliveryPlan(self,
            depotLocation, 
            deliveries, 
            commands):

        if len(deliveries) == 0:
            return DeliveryResult.DELIVERY_SUCCESS, 0.0

        self.__optimizer.optimizeDeliveryOrder(depotLocation, deliveries)
        
        totalRoute = []
        totalDistance   = 0.0
        for i in range(len(deliveries)-1):
            route = []
            gc1 = deliveries[i].location
            gc2 = deliveries[i+1].location
            result, distance = self.__router.generatePointToPointRoute(gc1, gc2, route)
            
            if result == DeliveryResult.BAD_COORD or result == DeliveryResult.NO_ROUTE:
                return result
            
            totalDistance += distance
            totalRoute    += route

        firstRoute = []
        lastRoute  = []
        firstDeliveryLocation = deliveries[0].location
        lastDeliveryLocation  = deliveries[-1].location
        result, distance1 = \
            self.__router.generatePointToPointRoute(depotLocation, firstDeliveryLocation, firstRoute)
        result, distance2 = \
            self.__router.generatePointToPointRoute(lastDeliveryLocation, depotLocation, lastRoute)
        
        totalDistance += distance1 + distance2
        totalRoute = firstRoute + totalRoute + lastRoute

        generateDeliveryCommand(totalRoute, commands, deliveries)

        return DeliveryResult.DELIVERY_SUCCESS, totalDistance