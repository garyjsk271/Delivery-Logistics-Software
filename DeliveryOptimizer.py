from PointToPointRouter import *
import random

TEMPERATURE = 100000
COOLINGRATE = 0.003

# Calculates the crow distance of the delivery route.
# @param depot The geospatial coordinate of the start & end location (i.e. the depot location)
# @param deliveries A list containing all the delivery requests to be fulfilled.
# @return The total crow distance (a double) through each point of delivery, in order.
def deliveryRouteCrowDistance(depot, deliveries):
    totalCrowDistance = 0.0
    for i in range(len(deliveries)-1):
        gc1 = deliveries[i].location
        gc2 = deliveries[i+1].location
        totalCrowDistance += distanceEarthMiles(gc1, gc2)
    totalCrowDistance += distanceEarthMiles(depot, deliveries[0].location)
    totalCrowDistance += distanceEarthMiles(deliveries[-1].location, depot)
    return totalCrowDistance

# Swaps the elements of a list
# @param list The list to be modified.
# @param i The index whose element shall be swapped.
# @param j The other index whose element shall be swapped.
# @post The list shall have the elments of two indices swapped. 
def swap(list, i, j):
    list[i], list[j] = list[j], list[i]

# Calculates the acceptance probability
# @param currentDistance The total distance of the current route.
# @param newDistance The total distance of the new route.
# @param temperature The current temperature.
# @return The calculated probability of whether to accept the new route.
def acceptanceProbability(currentDistance, newDistance, temperature):
    if newDistance < currentDistance:
        return 1.0
    return math.exp((currentDistance-newDistance)/temperature)

class DeliveryOptimizer:

    def __init__(self, streetmap):
        self.__router = PointToPointRouter(streetmap)

    # Optimizes the delivery process by Simulated Annealing.
    # @param depot The geospatial coordinate of the food depot, i.e. start location.
    # @param deliveries A list of delivery requests to be handled.
    # @return A tuple consisting of the old crow distance and the new
    #   crow distance (after optimization).
    def optimizeDeliveryOrder(self, depot, deliveries):
        if len(deliveries) < 2:
            return
            
        temperature = TEMPERATURE
        coolingRate = COOLINGRATE

        # Initialize current solution as a random solution.
        currentSolution = deliveries.copy()
        random.shuffle(currentSolution)

        # Keep track of the best solution so far.
        bestSolution = currentSolution.copy()
        bestDistance = deliveryRouteCrowDistance(depot, currentSolution)

        while temperature > 1:
            newSolution = currentSolution.copy()

            # generate 2 distinct random indices.
            index1 = random.randint(0, len(deliveries)-1)
            index2 = random.randint(0, len(deliveries)-1)
            while (index2 == index1):
                index2 = random.randint(0, len(deliveries)-1)
            
            # Swap the two random indices to create a new solution.
            swap(newSolution, index1, index2)
            
            # Get the energy states of both solutions (i.e. the distances)
            currentDistance = deliveryRouteCrowDistance(depot, currentSolution)
            newDistance     = deliveryRouteCrowDistance(depot, newSolution)
            
            # Determine if new solution should be accepted.
            rand = random.random()
            if acceptanceProbability(currentDistance, newDistance, temperature) > rand:
                currentSolution = newSolution
            
            # Track best solution so far.
            if currentDistance < bestDistance:
                bestSolution = currentSolution
                bestDistance = currentDistance

            # Cool temperature
            temperature *= 1-coolingRate

        oldCrowDistance = deliveryRouteCrowDistance(depot, deliveries)
        
        deliveries[:] = bestSolution

        return oldCrowDistance, bestDistance
        