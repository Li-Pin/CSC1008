from sqlalchemy import true
from queueClass import Queue
from math import radians, cos, sin, asin, sqrt
import json, os
from mergeSort import mergeSort

class Graph:
    file = open(os.path.abspath('JSON\junction.json'))
    data = json.load(file)
    locations = {}

    def __init__(self):
        self.setJunctionNode()
        self.v = len(self.locations)
        self.visited = []
        self.edgeGraph = dict()
        self.edges = [[-1 for i in range(self.v)] for j in range(self.v)]
        self.setEdge()

    def setJunctionNode(self):
        for i in self.data['junction']:
            self.locations.update({i['id']: [i['street_name'], i['lat'], i['lon'],True,i['edge']]})

    def setEdge(self):
        for i in range(len(self.locations)):
            lat1 = self.locations[i][1]
            lon1 = self.locations[i][2]
            for j in range(len(self.locations[i][4])):
                edgeID = self.locations[i][4][j]
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
            print(j, end=" ")
            pathArray.append(j)
            return
        self.printPath(parent, parent[j], pathArray)
        print(j, end=" ")
        pathArray.append(j)

    # A utility function to print
    # the constructed distance
    # array
    def printSolution(self, dist, parent, pathArray):

        src = 0
        print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)):
            if i == self.end:
                print("\n%d --> %d \t\t%f \t\t\t\t\t" % (self.start, i, dist[i]), end=" ")

                self.printPath(parent, i, pathArray)

    def dijkstra(self, start_vertex, end_vertex):
        self.end = int(end_vertex)
        self.start = int(start_vertex)
        D = {v: float('inf') for v in range(self.v)}
        D[self.start] = 0
        self.parent = {v: int(-1) for v in range(self.v)}
        pq = Queue()
        pq.enqueue((0, self.start))
        self.visited.clear()
        while not pq.isEmpty():
            (temp, current_vertex) = pq.dequeue()
            self.visited.append(current_vertex)

            for neighbor in range(self.v):
                if self.edges[current_vertex][neighbor] != -1:
                    distance = self.edges[current_vertex][neighbor]
                    if neighbor not in self.visited:
                        old_cost = D[neighbor]
                        new_cost = D[current_vertex] + distance
                        if new_cost < old_cost:
                            pq.enqueue((new_cost, neighbor))
                            D[neighbor] = new_cost
                            self.parent[neighbor] = current_vertex

        return D


# main


g = Graph()

# {0: 0, 1: 4, 2: 11, 3: 17, 4: 9, 5: 22, 6: 7, 7: 8, 8: 11}

# sorting edges in edgeGraph
for k in g.edgeGraph.keys():
    mergeSort(g.edgeGraph[k])
