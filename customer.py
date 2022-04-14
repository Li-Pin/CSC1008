from graphADT import g
from dijkstra import dijkstra


class Customer:
    # Constructor for customer's journey information
    def __init__(self, name):
        self.name = name
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    # to get customer's journey route and distance
    def getCustomerRide(self, start, end):
        self.start = start
        self.end = end

        # call dijkstra algorithm using customer's start and end points as parameters
        dij = dijkstra(g, self.start, self.end)

        # get journey distance from array in printSolution function
        self.pathDistance = g.printSolution(dij, g.parent, self.pathRoute)

        # return value when function called
        return self.pathRoute, self.pathDistance
