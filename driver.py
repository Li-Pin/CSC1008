import imp
from sqlalchemy import null
from graphADT import g
from flask import session as s
from djikstra import dijkstra
from graphADT import Graph

class Driver:

    def __init__(self, name, id):
        self.name = name  # replace with forms.get.(driver name)
        self.id = id
        self.start = None
        self.end = None
        self.pathRoute = []
        self.pathDistance = 0

    def startjob(self, start):  # start should be key of location
        graph = Graph().driverLocation
        if int(start) not in graph:
            graph.update({int(start): [self.id]})
            print(graph)
        else:
            graph[int(start)].append(self.id)
        


    def driverRoute(self, driverLoc, customerLoc):
        self.start = driverLoc
        self.end = customerLoc
        C = dijkstra(g, str(self.start), self.end)
        g.printSolution(C, g.parent, self.pathRoute)
        self.pathDistance = g.printSolution(C, g.parent, self.pathRoute)
        return self.pathRoute, self.pathDistance
