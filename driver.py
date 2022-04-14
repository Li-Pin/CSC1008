from sqlalchemy import null
from flask import session as s
from graphADT import g
from dijkstra import dijkstra


class Driver:
    # Driver class used to store driver details pathRoute = route for driver, pathDistance = distance
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    # Running dijsktra to calculate shortest path from driver to customer location and return Path and Distance.
    def driverRoute(self, driverLoc, customerLoc):
        self.start = driverLoc
        self.end = customerLoc
        C = dijkstra(g, str(self.start), self.end)
        self.pathDistance = g.printSolution(C, g.parent, self.pathRoute)
        return self.pathRoute, self.pathDistance
