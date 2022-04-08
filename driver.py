from graphADT import g


class driver:
    def __init__(self):
        self.name = 'Ah teck'  # replace with forms.get.(driver name)
        self.id = 'ahteckSiol'  # replace with forms.get.(driverid)
        self.start = None
        self.end = None
        self.pathRoute = []

    def startjob(self, start): # start should be key of location
        self.start = start
        g.locations[start][3] = True

    def driverRoute(self, customerLoc):
        C = g.dijkstra(str(self.start), customerLoc)
        g.printSolution(C, g.parent, self.pathRoute)


