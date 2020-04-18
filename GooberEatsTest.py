import unittest

from provided import *
from ExpandableHashMap import *
from StreetMap import *
from PointToPointRouter import *
from DeliveryOptimizer import *
from DeliveryPlanner import *

# Note: unittest DOES NOT run the testcases in the order they are defined!

hashtables     = [ExpandableHashMap() for _ in range(6)]
imaginationMap = StreetMap()
streetmap      = StreetMap()

streetmap.load('mapdata.txt')   # will throw exception if load unsuccessful
imaginationMap.load('imaginationWorldData.txt')

router1 = PointToPointRouter(imaginationMap)
router2 = PointToPointRouter(streetmap)

optimizer1 = DeliveryOptimizer(imaginationMap)
optimizer2 = DeliveryOptimizer(streetmap)

planner1 = DeliveryPlanner(imaginationMap)
planner2 = DeliveryPlanner(streetmap)

def routeContainsTheseStreets(route, expectedNames):
    names = ''
    for segment in route:
        names += ' ' + segment.name
    return names[1:] == expectedNames

def routeContainsTheseGeoCoords(route, expectedGeoCoords):
    coordinates = expectedGeoCoords.split(' ')
    i = 0
    j = 0
    while j+3 < len(coordinates):
        if route[i].start != GeoCoord(coordinates[j], coordinates[j+1]) or\
           route[i].end   != GeoCoord(coordinates[j+2], coordinates[j+3]):

           return False
        j += 2
        i += 1
    return True

def printDeliveryCommands(commands):
    print()
    for command in commands:
        print(command.description() )

class utilityFunctionTest(unittest.TestCase):
    def test_getGeoCoord(self):
        gc1, gc2 = getGeoCoords("34.0547000 -118.4794734 34.0544590 -118.4801137\n")
        self.assertEqual(gc1, GeoCoord("34.0547000", "-118.4794734") )
        self.assertEqual(gc2, GeoCoord("34.0544590", "-118.4801137") )

    def test_routeDistance(self):
        start = GeoCoord('0', '0')
        end   = GeoCoord('2', '3')
        route = []
        
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertEqual(distance, segmentDistance(route[0]) + segmentDistance(route[1]), routeDistance(route) )
        self.assertEqual(route[0].name, 'A Street')
        self.assertEqual(route[1].name, 'A Street')

    def test_routeContainsTheseGeoCoords(self):
        start = GeoCoord('0', '0')
        end   = GeoCoord('1', '1')
        route = []
        
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 1)
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1') )

        end = GeoCoord('2', '3')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3') )

        end = GeoCoord('5', '6')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 3)
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3 5 6') )

class ExpandableHashMapTest(unittest.TestCase):

    def test_initialization(self):
        self.assertEqual(hashtables[0]._ExpandableHashMap__capacity, 8)
        self.assertEqual(hashtables[0]._ExpandableHashMap__size, 0)
        self.assertEqual(hashtables[0]._ExpandableHashMap__indexOfNextPrime, 0)

    def test_tableInitializedWithEmptyLists(self):
        for theList in hashtables[0]._ExpandableHashMap__table:
            self.assertEqual(theList, [])

    def test_associate_find(self):
        self.assertIsNone(hashtables[0].find('cookie'))
        self.assertIsNone(hashtables[1].find(None))
        hashtables[1].associate('cookie', 'chocolate chip')
        hashtables[2].associate('apple', 'fruit')
        self.assertEqual(hashtables[2].find('apple'), 'fruit')
        self.assertNotEqual(hashtables[2].find('apple'), 'carbohydrate source')
        hashtables[2].associate('apple', 'carbohydrate source')
        self.assertNotEqual(hashtables[2].find('apple'), 'fruit')
        self.assertEqual(hashtables[2].find('apple'), 'carbohydrate source')
        hashtables[2].associate('salmon', 'great fatty acid source')
        self.assertEqual(hashtables[2].find('salmon'), 'great fatty acid source')
        hashtables[3].associate('Carey', 'rock climber')
        self.assertEqual(hashtables[3].find('Carey'), 'rock climber')
        self.assertIsNot(hashtables[3].find('Carey'), 'principal engineer')
        hashtables[3].associate('Carey', 'principal engineer')
        self.assertIsNot(hashtables[3].find('Carey'), 'rock climber')
        self.assertEqual(hashtables[3].find('Carey'), 'principal engineer')
        hashtables[3].associate('Kee', 'newb coder')
        self.assertEqual(hashtables[3].find('Kee'), 'newb coder')
        self.assertIsNone(hashtables[3].find('kee'))
        hashtables[3].associate('Gary', 'a coder')
        self.assertEqual(hashtables[3].find('Gary'), 'a coder')
        for i in range(4):
            hashtables[4].associate(i, str(i))  
        for i in range(5):
            hashtables[5].associate(i, str(i))
        self.test_size()

    def test_size(self):
        for i in range(len(hashtables)):
            self.assertEqual(hashtables[i].size(), i)
    
    def test_capacity(self):
        for i in range(5):
            self.assertEqual(hashtables[i]._ExpandableHashMap__capacity, 8)
        self.assertEqual(hashtables[5]._ExpandableHashMap__capacity, 11)

    def test_getitem(self):
        self.assertIsNone(hashtables[0]['should return None'], None)
        self.assertEqual(hashtables[1]['cookie'], 'chocolate chip')
        self.assertEqual(hashtables[2]['apple'], 'carbohydrate source')
        self.assertEqual(hashtables[2]['salmon'], 'great fatty acid source')
        self.test_size()

    def test_setitem(self):
        hashtables[1]['cookie'] = 'dessert'
        self.assertEqual(hashtables[1]['cookie'], 'dessert')
        hashtables[2]['salmon'] = 'fish'
        hashtables[2]['apple']  = 'fruit'
        self.assertEqual(hashtables[1]['cookie'], 'dessert')
        self.assertEqual(hashtables[1]['cookie'], 'dessert')
        self.test_size()

class StreetMapTest(unittest.TestCase):
    
    def test_getSegmentsThatStartWith(self):   
        segments = []
        gc = GeoCoord("34.0547000", "-118.4794734")
        streetmap.getSegmentsThatStartWith(gc, segments)
        self.assertEqual(len(segments), 1)

        segments.clear()
        gc = GeoCoord("34.0852898", "-118.4954341")
        streetmap.getSegmentsThatStartWith(gc, segments)
        self.assertEqual(len(segments), 1)

        segments.clear()
        gc = GeoCoord("34.0555356", "-118.4798135")
        streetmap.getSegmentsThatStartWith(gc, segments)
        self.assertEqual(len(segments), 2)

        segments.clear()
        gc = GeoCoord("34.0544590", "-118.4801137")
        streetmap.getSegmentsThatStartWith(gc, segments)
        self.assertEqual(len(segments), 3)

        segments.clear()
        gc = GeoCoord("34.0420561", "-118.5011699")
        streetmap.getSegmentsThatStartWith(gc, segments)
        self.assertEqual(len(segments), 3)

        segments.clear()
        gc = GeoCoord("34.0356922", "-118.4937358")
        streetmap.getSegmentsThatStartWith(gc, segments)
        self.assertEqual(len(segments), 4)

    def test_load(self):
        with self.assertRaises(FileNotFoundError):
            streetmap.load("BAD_FILE_NAME")

class PointToPointRouterTest(unittest.TestCase):

    def test_getSegmentsThatStartWith(self):
        start    = GeoCoord('0', '0')
        end      = GeoCoord('inf', 'inf')
        route    = []
        
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.BAD_COORD, result)
        self.assertEqual(distance, -1)

        end = GeoCoord('43', '43')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.BAD_COORD, result)
        self.assertEqual(distance, -1)

        end = start
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(distance, 0)
        self.assertEqual(len(route), 0)
        self.assertTrue(routeContainsTheseGeoCoords(route, '') )

        end = GeoCoord('1', '1')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(distance, distanceEarthMiles(start, end))
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'A Street')
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1') )

        end = GeoCoord('2', '3')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertEqual(distance, segmentDistance(route[0]) + segmentDistance(route[1]) )
        self.assertEqual(route[0].name, 'A Street')
        self.assertEqual(route[1].name, 'A Street')
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3') )

        end = GeoCoord('3', '2')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        expectedStreetNames = 'A Street A Street B Street'
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 3)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3 3 2') )

        end = GeoCoord('4', '2')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        expectedStreetNames = 'A Street A Street B Street B Street'
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 4)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3 3 2 4 2') )

        end = GeoCoord('5', '6')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        expectedStreetNames = 'A Street A Street A Street'
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 3)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3 5 6') )

        end = GeoCoord('6', '7')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        expectedStreetNames = 'A Street A Street A Street C Street'
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 4)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 0 1 1 2 3 5 6 6 7') )
        
        start = GeoCoord('0', '19')
        end   = GeoCoord('0', '20')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        expectedStreetNames = 'Westwood'
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 1)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 19 0 20') )

        end = GeoCoord('10', '30')
        result, distance = router1.generatePointToPointRoute(start, end, route)
        expectedStreetNames = 'Westwood Wilshire'
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, '0 19 0 20 10 30') )
        
        start = GeoCoord('30', '5')
        end   = GeoCoord('20', '40')
        expectedStreetNames = 'Reli Wormhole'
        expectedGeoCoords   = '30 5 33 33 20 40'
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, expectedGeoCoords) )

        start = GeoCoord('6', '7')
        end   = GeoCoord('53', '20')
        expectedStreetNames = 'C Street A Street A Street A Street Reli Reli'
        expectedGeoCoords   = '6 7 5 6 2 3 1 1 0 0 30 5 53 20'
        result, distance = router1.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 6)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, expectedGeoCoords) )

        start = GeoCoord('34.0420561', '-118.5011699')
        end   = GeoCoord('34.0411467', '-118.5001646')
        expectedStreetNames = '17th Street 17th Street'
        expectedGeoCoords   = '34.0420561 -118.5011699 34.0419265 -118.5010322 34.0411467 -118.5001646'
        result, distance = router2.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, expectedGeoCoords) )

        end = GeoCoord('34.0411726', '-118.5019849')
        expectedStreetNames = '17th Street West San Vicente Boulevard'
        expectedGeoCoords   = \
            '34.0420561 -118.5011699 34.0419265 -118.5010322 34.0411726 -118.5019849'
        result, distance = router2.generatePointToPointRoute(start, end, route)
        self.assertEqual(DeliveryResult.DELIVERY_SUCCESS, result)
        self.assertEqual(len(route), 2)
        self.assertEqual(distance, routeDistance(route) )
        self.assertTrue(routeContainsTheseStreets(route, expectedStreetNames) )
        self.assertTrue(routeContainsTheseGeoCoords(route, expectedGeoCoords) )

class DeliveryOptimizerTest(unittest.TestCase):
    def test_optimizeDeliverOrder(self):
        deliveries = [
            DeliveryRequest('', GeoCoord('2','3') ),
            DeliveryRequest('', GeoCoord('42','42') ),
            DeliveryRequest('', GeoCoord('0','0') )
        ]
        depot = GeoCoord('30', '5')
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        deliveries.append(DeliveryRequest('', GeoCoord('0','19') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        deliveries.append(DeliveryRequest('', GeoCoord('33','33') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        deliveries.append(DeliveryRequest('', GeoCoord('5','6') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        deliveries.append(DeliveryRequest('', GeoCoord('53','20') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        deliveries.append(DeliveryRequest('', GeoCoord('0','20') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        deliveries.append(DeliveryRequest('', GeoCoord('25','40') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        depot = GeoCoord('0', '0')
        deliveries.append(DeliveryRequest('', GeoCoord('6','7') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

        depot = GeoCoord('42', '42')
        deliveries.append(DeliveryRequest('', GeoCoord('6','7') ) )
        oldCrowDistance, newCrowDistance = optimizer1.optimizeDeliveryOrder(depot, deliveries) 
        self.assertLessEqual(newCrowDistance, oldCrowDistance)

        print('Old Crow Distance: {0}\tNew Crow Distance: {1}'.format(oldCrowDistance, newCrowDistance))

class DeliveryPlannerTest(unittest.TestCase):
    def test_generateDeliveryPlan(self):
        depot = GeoCoord('5','6')
        deliveries = []
        commands = []
        result, totalDistance = planner1.generateDeliveryPlan(depot, deliveries, commands)
        self.assertEqual(result, DeliveryResult.DELIVERY_SUCCESS)
        self.assertEqual(totalDistance, 0.0)
        printDeliveryCommands(commands)
        print('Total Distance: {0}'.format(totalDistance) )

        deliveries.append(DeliveryRequest('salmon', GeoCoord('0', '0') ) )
        result, totalDistance = planner1.generateDeliveryPlan(depot, deliveries, commands)
        self.assertEqual(result, DeliveryResult.DELIVERY_SUCCESS)
        self.assertGreater(totalDistance, 0)
        printDeliveryCommands(commands)
        print('Total Distance: {0}'.format(totalDistance) )

        deliveries.append(DeliveryRequest('fillet mignon', GeoCoord('4', '2') ) )
        result, totalDistance = planner1.generateDeliveryPlan(depot, deliveries, commands)
        self.assertEqual(result, DeliveryResult.DELIVERY_SUCCESS)
        self.assertGreater(totalDistance, 1000)
        printDeliveryCommands(commands)
        print('Total Distance: {0}'.format(totalDistance) )

        deliveries.append(DeliveryRequest('pho', GeoCoord('42', '42') ) )
        result, totalDistance = planner1.generateDeliveryPlan(depot, deliveries, commands)
        self.assertEqual(result, DeliveryResult.DELIVERY_SUCCESS)
        self.assertGreater(totalDistance, 1247)
        printDeliveryCommands(commands)
        print('Total Distance: {0}'.format(totalDistance) )

if __name__ == '__main__':
    unittest.main()