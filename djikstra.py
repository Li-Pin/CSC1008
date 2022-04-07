from queue import PriorityQueue, Queue


class Graph:
    locations = {
        0: ['Ang Mo Kio', 1.352083, 103.819839, False],
        1: ['Ang Mo Kio', 1.352083, 103.819839, True],
        2: ['Ang Mo Kio', 1.352083, 103.819839, False],
        3: ['Ang Mo Kio', 1.352083, 103.819839, False],
        4: ['Ang Mo Kio', 1.352083, 103.819839, False],
        5: ['Ang Mo Kio', 1.352083, 103.819839, False],
        6: ['Ang Mo Kio', 1.352083, 103.819839, False],
        7: ['Ang Mo Kio', 1.352083, 103.819839, False],
        8: ['Ang Mo Kio', 1.352083, 103.819839, True]
    }

    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []
        self.edgeGraph = dict()

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
    # def mergeSort(self):
    #     for k in self.edgeGraph.keys():
    #         if len(self.edgeGraph) > 1:
    #
    #             # Finding the mid of the array
    #             mid = len(arr) // 2
    #
    #             # Dividing the array elements
    #             L = arr[:mid]
    #
    #             # into 2 halves
    #             R = arr[mid:]
    #
    #             # Sorting the first half
    #             self.mergeSort(L)
    #
    #             # Sorting the second half
    #             self.mergeSort(R)
    #
    #             i = j = k = 0
    #
    #             # Copy data to temp arrays L[] and R[]
    #             while i < len(L) and j < len(R):
    #                 if L[i] < R[j]:
    #                     arr[k] = L[i]
    #                     i += 1
    #                 else:
    #                     arr[k] = R[j]
    #                     j += 1
    #                 k += 1
    #
    #             # Checking if any element was left
    #             while i < len(L):
    #                 arr[k] = L[i]
    #                 i += 1
    #                 k += 1
    #
    #             while j < len(R):
    #                 arr[k] = R[j]
    #                 j += 1
    #                 k += 1
    #
    #     self.edgeGraph
    #     for k in self.edgeGraph.keys():

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
        pq.put((0, self.start))
        self.visited.clear()
        while not pq.empty():
            (temp, current_vertex) = pq.get()
            self.visited.append(current_vertex)

            for neighbor in range(self.v):
                if self.edges[current_vertex][neighbor] != -1:
                    distance = self.edges[current_vertex][neighbor]
                    if neighbor not in self.visited:
                        old_cost = D[neighbor]
                        new_cost = D[current_vertex] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbor))
                            D[neighbor] = new_cost
                            self.parent[neighbor] = current_vertex

        return D

def finddriver(graph, s):
    driverisat = ''
    if graph.locations[s][3]==True:
        driverisat=s
        return driverisat
    visited = {}
    bfs_traversal_output = []
    queue = Queue()
    for location in graph.edgeGraph.keys():
        visited[location] = False
    visited[s] = True
    queue.put(s)

    print(graph.edgeGraph[s])
    while not queue.empty():
        u = queue.get()
        bfs_traversal_output.append(u)
        print('test')
        for v in graph.edgeGraph[u]:
            if not visited[v[0]]:
                if v[2] == True:
                    print('driver found at graph')
                    print(v[0])
                    driverisat = v[0]
                    break
                visited[v[0]] = True
                queue.put(v[0])
                # for j in graph.vertices.keys():
    print(driverisat)
    print(bfs_traversal_output)
    return driverisat


g = Graph(9)
g.add_edge(0, 1, 4)
g.add_edge(0, 6, 7)
g.add_edge(1, 6, 11)
g.add_edge(1, 7, 20)
g.add_edge(1, 2, 9)
g.add_edge(2, 3, 6)
g.add_edge(2, 4, 2)
g.add_edge(3, 4, 10)
g.add_edge(3, 5, 5)
g.add_edge(4, 5, 15)
g.add_edge(4, 7, 1)
g.add_edge(4, 8, 5)
g.add_edge(5, 8, 12)
g.add_edge(6, 7, 1)
g.add_edge(7, 8, 3)
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
driverStart = int(finddriver(g, int(start)))
print('Driver is at', driverStart)
C = g.dijkstra(str(driverStart), start)
g.printSolution(C, g.parent)
