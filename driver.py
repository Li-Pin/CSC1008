from sqlalchemy import null
from graphADT import g
import random


class driver:

    def __init__(self):
        self.name = 'Ah teck'  # replace with forms.get.(driver name)
        self.id = 'ahteckSiol'  # replace with forms.get.(driverid)
        self.start = None
        self.end = None
        self.pathRoute = []
        self.assignDriverLocation()

    def assignDriverLocation(self):
        print(g.driver)
        for i in range(len(g.driver)):
            ranLocation = random.randint(0, len(g.locations))
            if ranLocation not in g.driverLocation:
                g.driverLocation.update({ranLocation: [i+1]})
            else:
                g.driverLocation[ranLocation].append(i+1)
        print(g.driverLocation)

    def startjob(self, start): # start should be key of location
        self.start = start
        g.locations[start][3] = True

    def driverRoute(self, customerLoc):
        C = g.dijkstra(str(self.start), customerLoc)
        g.printSolution(C, g.parent, self.pathRoute)



driver()