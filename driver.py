from djikstra import g


class customer:

    def __init__(self):
        self.name = 'Ah teck'
        self.id = 'ahteckSiol'
        self.start = None
        self.end = None
        self.pathRoute = []


newCustomer = customer()
newCustomer.start = input('Enter Start Point: ')
newCustomer.end = input('Enter End Point: ')
C = g.dijkstra(newCustomer.start, newCustomer.end)
g.printSolution(C, g.parent, newCustomer.pathRoute)
maxDriverDistance = input('Enter max driver distance: ')
print(newCustomer.pathRoute)
