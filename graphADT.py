import json
import os
from math import radians, cos, sin, asin, sqrt
from mergeSort import mergeSort


class Graph:
    # Getting path file path of junction.json
    file = open(os.path.abspath('JSON\junction.json'))
    # Loading json file into data
    data = json.load(file)

    def __init__(self):
        # Create empty dict edgeGraph, locations, drivers, driversLocation
        self.edgeGraph = dict()
        self.locations = dict()
        self.drivers = dict()
        self.driverLocation = dict()
        # Calling function to initial junction into locations dict
        self.setJunctionNode()
        # Store the length of vertex in V
        self.v = len(self.locations)
        # Create a visited array
        self.visited = []
        # Create edges 2D array
        self.edges = [[-1 for i in range(self.v)] for j in range(self.v)]
        # Call function setEdges
        self.setEdge()

    # Retrieve data from json  and add into locations dict
    def setJunctionNode(self):
        for i in self.data['junction']:
            self.locations.update({i['id']: [i['street_name'], i['lat'], i['lon'], i['edge']]})

    # Set the lat, lon of within 2 points and find the distance between all neighbour vertex
    def setEdge(self):
        for i in range(len(self.locations)):
            # Start location
            lat1 = self.locations[i][1]
            lon1 = self.locations[i][2]
            for j in range(len(self.locations[i][3])):
                # End location
                edgeID = self.locations[i][3][j]
                lat2 = self.locations[edgeID][1]
                lon2 = self.locations[edgeID][2]
                # Calculate the distance between two point
                distance = self.getDistance(lon1, lat1, lon2, lat2)
                # Call add_edge function
                self.add_edge(i, edgeID, distance)

    # Calculate the distance using lat, lon
    def getDistance(self, lon1, lat1, lon2, lat2):
        # Convert the latitudes and longitudes from degree to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        # Haversine Formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in KM.
        r = 6371

        return c * r

    # Add weight to edges, if location 1 to location 2 or location 2 to location 1
    # not in edgeGraph then add to edgeGraph
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

    # Function to print shortest path from source to j using parent array
    def printPath(self, parent, j, pathArray):
        # Base Case : If j is source
        if parent[j] == -1:
            pathArray.append(j)
            return
        self.printPath(parent, parent[j], pathArray)

        pathArray.append(j)

    # A utility function to print the constructed distance array
    def printSolution(self, dist, parent, pathArray):
        for i in range(0, len(dist)):
            if i == self.end:
                self.printPath(parent, i, pathArray)
                return dist[i]


g = Graph()

# sorting edges in edgeGraph
for k in g.edgeGraph.keys():
    mergeSort(g.edgeGraph[k])
