from graphADT import g


class driver:
    def __init__(self):
        self.name = 'Ah teck'  # replace with forms.get.(driver name)
        self.id = 'ahteckSiol' # re
        self.start = None
        self.end = None
        self.pathRoute = []

    def startjob(self, start): # start should be key of location
        self.start = start
        g.locations[start][3] = True

    def driverRoute(self, customerLoc):
        C = g.dijkstra(str(self.start), customerLoc)
        g.printSolution(C, g.parent, self.pathRoute)


# newCustomer = customer()
# newCustomer.start = input('Enter Start Point: ')
# newCustomer.end = input('Enter End Point: ')
# C = g.dijkstra(newCustomer.start, newCustomer.end)
# g.printSolution(C, g.parent, newCustomer.pathRoute)
# maxDriverDistance = input('Enter max driver distance: ')
# print(newCustomer.pathRoute)
