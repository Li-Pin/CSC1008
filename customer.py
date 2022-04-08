from djikstra import g


class customer:

    def __init__(self):
        self.name = 'tan yi'
        self.id = 'ty01'
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


from queue import Queue
from mergeSort import mergeSort

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



    # def minDistance(self, dist, queue):
    #     # Initialize min value and min_index as -1
    #     minimum = float("Inf")
    #     min_index = -1
    #
    #     # from the dist array,pick one which
    #     # has min value and is till in queue
    #     for i in range(len(dist)):
    #         if dist[i] < minimum and i in queue:
    #             minimum = dist[i]
    #             min_index = i
    #     return min_index

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
                print("\n%d --> %d \t\t%d \t\t\t\t\t" % (self.start, i, dist[i]), end=" ")

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



#main

driverPath = []
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
g.add_edge(4, 8, 7)
g.add_edge(5, 8, 12)
g.add_edge(6, 7, 1)
g.add_edge(7, 8, 3)


# {0: 0, 1: 4, 2: 11, 3: 17, 4: 9, 5: 22, 6: 7, 7: 8, 8: 11}

# sorting edges in edgeGraph
for k in g.edgeGraph.keys():
    mergeSort(g.edgeGraph[k])

