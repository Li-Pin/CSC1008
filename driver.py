from sqlalchemy import null
from graphADT import g
import random


class driver:

    driver = {
        1 : ["Peter Low", 91234457,"SKA1154C"],
        2 : ["Alex Tan", 91234457,"SKA4554C"],
        3 : ["Jess Low", 91234457,"SKA8888C"],
        4 : ["Felix Tan", 88961234,"SKG4894C"],
        5 : ["Lim Tan Lau", 89551445,"STH4354C"]
    }

    def __init__(self):
        self.name = 'Ah teck'  # replace with forms.get.(driver name)
        self.id = 'ahteckSiol'  # replace with forms.get.(driverid)
        self.start = None
        self.end = None
        self.driverLocation = dict()
        self.pathRoute = []
        self.assignDriverLocation()

    def assignDriverLocation(self):
        for i in range(len(self.driver)):
            ranLocation = random.randint(0, len(g.locations))
            if ranLocation not in self.driverLocation:
                self.driverLocation.update({ranLocation: [i+1]})
            else:
                self.driverLocation[ranLocation].append(i+1)
        print(self.driverLocation)

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
# print(newCustomer.pathRoute)clear

driver()