import json
import os
from math import radians, cos, sin, asin, sqrt

from mergeSort import mergeSort


class Graph:
    file = open(os.path.abspath('JSON\junction.json'))
    data = json.load(file)

    

    def __init__(self):
        self.edgeGraph = dict()
        self.locations = dict()
        self.drivers = dict()
        self.driverLocation = dict()
        self.setJunctionNode()
        self.v = len(self.locations)
        self.visited = []
        self.edges = [[-1 for i in range(self.v)] for j in range(self.v)]
        self.setEdge()
        # self.assignDriverLocation()

    def setJunctionNode(self):
        for i in self.data['junction']:
            self.locations.update({i['id']: [i['street_name'], i['lat'], i['lon'], i['edge']]})

    def setEdge(self):
        for i in range(len(self.locations)):
            lat1 = self.locations[i][1]
            lon1 = self.locations[i][2]
            for j in range(len(self.locations[i][3])):
                edgeID = self.locations[i][3][j]
                lat2 = self.locations[edgeID][1]
                lon2 = self.locations[edgeID][2]
                distance = self.getDistance(lon1, lat1, lon2, lat2)
                self.add_edge(i, edgeID, distance)

    def getDistance(self, lon1, lat1, lon2, lat2):
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in KM.
        r = 6371

        return c * r

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight
        isDirected = False
        if u not in self.edgeGraph:
            self.edgeGraph[u] = []

        if v not in self.edgeGraph:
            self.edgeGraph[v] = []
            # Maintain Adjacency List
            # Maintain the data in List as Tuple, where we have adjacent vertex and weight
            self.edgeGraph[u].append((v, weight, self.locations[v][3]))
        if not isDirected:
            self.edgeGraph[v].append((u, weight, self.locations[u][3]))

    # Function to print shortest path
    # from source to j
    # using parent array
    def printPath(self, parent, j, pathArray):

        # Base Case : If j is source
        if parent[j] == -1:
            pathArray.append(j)
            return
        self.printPath(parent, parent[j], pathArray)

        pathArray.append(j)

    # A utility function to print
    # the constructed distance
    # array
    def printSolution(self, dist, parent, pathArray):

        src = 0
        for i in range(0, len(dist)):
            if i == self.end:
                self.printPath(parent, i, pathArray)
                return dist[i]


g = Graph()

# sorting edges in edgeGraph
for k in g.edgeGraph.keys():
    mergeSort(g.edgeGraph[k])
