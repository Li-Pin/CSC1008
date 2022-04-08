from queue import Queue
from math import radians, cos, sin, asin, sqrt
import json, os

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
            self.locations.update({i['id']:[i['street_name'],i['lat'],i['lon'],i['edge']]}) 
    
    def setEdge(self):
        for i in range(len(self.locations)):
            lat1 = self.locations[i][1]
            lon1 = self.locations[i][2]
            for j in range(len(self.locations[i][3])):
                edgeID = self.locations[i][3][j]
                lat2 = self.locations[edgeID][1]
                lon2 = self.locations[edgeID][2]
                distance = self.getDistance(lon1,lat1,lon2,lat2)
                self.add_edge(i, edgeID, distance)
            

    def getDistance(self,lon1,lat1,lon2,lat2):
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
        c = 2 * asin(sqrt(a))
    
        # Radius of earth in KM.
        r = 6371
      
        return c*r
     

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
            
    def mergeSort(self, edgeGraph):
            if len(edgeGraph) > 1:

                # Finding the mid of the array
                mid = len(edgeGraph) // 2

                # Dividing the array elements
                L = edgeGraph[:mid]

                # into 2 halves
                R = edgeGraph[mid:]

                # Sorting the first half
                self.mergeSort(L)

                # Sorting the second half
                self.mergeSort(R)

                i = j = o = 0

                # Copy data to temp arrays L[] and R[]
                while i < len(L) and j < len(R):
                    if L[i][1] < R[j][1]:
                        edgeGraph[o] = L[i]
                        i += 1
                    else:
                        edgeGraph[o] = R[j]
                        j += 1
                    o += 1

                # Checking if any element was left
                while i < len(L):
                    edgeGraph[o] = L[i]
                    i += 1
                    o += 1

                while j < len(R):
                    edgeGraph[o] = R[j]
                    j += 1
                    o += 1


    def minDistance(self, dist, queue):
        # Initialize min value and min_index as -1
        minimum = float("Inf")
        min_index = -1

        # from the dist array,pick one which
        # has min value and is till in queue
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    # Function to print shortest path
    # from source to j
    # using parent array
    def printPath(self, parent, j):

        # Base Case : If j is source
        if parent[j] == -1:
            print(j, end=" ")
            return
        self.printPath(parent, parent[j])
        print(j, end=" ")

    # A utility function to print
    # the constructed distance
    # array
    def printSolution(self, dist, parent):

        src = 0
        print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)):
            if i == self.end:
                print("\n%d --> %d \t\t%d \t\t\t\t\t" % (self.start, i, dist[i]), end=" ")
                self.printPath(parent, i)

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

def finddriver(graph, s, max):

    driverisat = 'No driver'
    if graph.locations[s][3]==True:
        driverisat=s
        return driverisat
    visited = {}
    bfs_traversal_output = []
    queue = Queue()
    for location in graph.edgeGraph.keys():
        visited[location] = False
    visited[s] = True
    queue.enqueue(s)

    print(graph.edgeGraph[s])
    while not queue.isEmpty():
        u = queue.dequeue()
        bfs_traversal_output.append(u)
        print('test')
        for v in graph.edgeGraph[u]:
            if not visited[v[0]]:
                if v[2] == True and v[1] < max:
                    print('driver found at graph')
                    print(v[0])
                    driverisat = v[0]
                    break
                visited[v[0]] = True
                queue.enqueue(v[0])
                # for j in graph.vertices.keys():


    return driverisat


g = Graph()
print(len(g.edges))
print(len(g.locations))
start = input('Enter Start Point: ')
end = input('Enter End Point: ')

C = g.dijkstra(start, end)
g.printSolution(C, g.parent)
print()
print(g.edgeGraph[int(start)])

for i in range(len(g.edges)):
    position = -1
    for j in g.edges[i]:
        position += 1
        if j > 0:
            print(i, ' has edge to', position)
# {0: 0, 1: 4, 2: 11, 3: 17, 4: 9, 5: 22, 6: 7, 7: 8, 8: 11}
print()
for vertex in range(len(C)):
    print("Distance from vertex ", start, " to vertex", vertex, "is", C[vertex])
for k in g.edgeGraph.keys():
    g.mergeSort(g.edgeGraph[k])
max = input('Enter max driver distance')
driverStart = finddriver(g, int(start), int(max))
if driverStart != 'No driver':
    print('Driver is at', int(driverStart))
    C = g.dijkstra(str(driverStart), start)
    g.printSolution(C, g.parent)
else:
    print('No driver nearby! ')
