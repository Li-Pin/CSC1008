from graphADT import g
from djikstra import dijkstra


class Customer:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    def getCustomerRide(self):
        self.start = input('Enter Start Point: ')  # to replace with form.get.(=start)
        self.end = input('Enter End Point: ')  # to replace with form.get.(=end)
        C = dijkstra(g, self.start, self.end)
        self.pathDistance = g.printSolution(C, g.parent, self.pathRoute)
        return self.pathRoute, self.pathDistance
