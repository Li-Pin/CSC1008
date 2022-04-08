from graphADT import g
from djikstra import dijkstra


class Customer:
    baseFare = 4.05
    KMPrice = 0.7

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.start = None
        self.end = None
        self.pathRoute = []

    def getCustomerRide(self):
        self.start = input('Enter Start Point: ')  # to replace with form.get.(=start)
        self.end = input('Enter End Point: ')  # to replace with form.get.(=end)
        C = dijkstra(g, self.start, self.end)
        distance = g.printSolution(C, g.parent, self.pathRoute)
        maxDriverDistance = input('Enter max driver distance: ')
        print(self.pathRoute)
        print('your is distance is: ', distance)
        print('price will be :', 4.05 + distance * 0.7)
        return self.pathRoute
