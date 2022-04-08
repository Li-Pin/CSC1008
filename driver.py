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


    def startjob(self, start): # start should be key of location
        self.start = start
        g.locations[start][3] = True
        # g.driver append driver name
        # g.driverlocation append if no key exist, new key [driverID] else new key = location : [driverID]

    def driverRoute(self, customerLoc):
        C = g.dijkstra(str(self.start), customerLoc)
        g.printSolution(C, g.parent, self.pathRoute)
