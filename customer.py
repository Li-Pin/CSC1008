from graphADT import g
from djikstra import dijkstra


class Customer:

    def __init__(self, name):
        self.name = name
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    def getCustomerRide(self,start,end):
        self.start = start
        self.end = end
        C = dijkstra(g, self.start, self.end)
        self.pathDistance = g.printSolution(C, g.parent, self.pathRoute)
        return self.pathRoute, self.pathDistance
