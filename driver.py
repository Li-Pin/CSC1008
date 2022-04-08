from sqlalchemy import null
from graphADT import g
import random
from djikstra import dijkstra


class Driver:

    def __init__(self, name):
        self.name = name  # replace with forms.get.(driver name)
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    def startjob(self, start):  # start should be key of location
        self.start = start
        # g.driver append driver name
        # g.driverlocation append if no key exist, new key [driverID] else new key = location : [driverID]


    def driverRoute(self, driverLoc, customerLoc):
        self.start = driverLoc
        self.end = customerLoc
        C = dijkstra(g, str(self.start), self.end)
        g.printSolution(C, g.parent, self.pathRoute)
        self.pathDistance = g.printSolution(C, g.parent, self.pathRoute)
        return self.pathRoute, self.pathDistance
