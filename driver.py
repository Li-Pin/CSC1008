import imp
from sqlalchemy import null
from flask import session as s
from graphADT import g
from djikstra import dijkstra


class Driver:

    def __init__(self, name, id):
        self.name = name  # replace with forms.get.(driver name)
        self.id = id
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    # def startjob(self, start):  # start should be key of location
    #     graph = g.driverLocation
    #     if int(start) not in graph:
    #         graph.update({int(start): [self.id]})
    #         print(graph)
    #     else:
    #         graph[int(start)].append(self.id)

    def driverRoute(self, driverLoc, customerLoc):
        self.start = driverLoc
        self.end = customerLoc
        C = dijkstra(g, str(self.start), self.end)
        self.pathDistance = g.printSolution(C, g.parent, self.pathRoute)
        return self.pathRoute, self.pathDistance
