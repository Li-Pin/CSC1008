from queue import PriorityQueue
class Graph:
    locations = {
        1: ['Ang Mo Kio', 1.352083, 103.819839],
        2: ['Ang Mo Kio', 1.352083, 103.819839],
        3: ['Ang Mo Kio', 1.352083, 103.819839]
    }

    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight
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

    def dijkstra(self, start_vertex,end_vertex):
        self.end=int(end_vertex)
        self.start=int(start_vertex)
        D = {v: float('inf') for v in range(self.v)}
        D[self.start] = 0
        self.parent = {v: int(-1) for v in range(self.v)}
        pq = PriorityQueue()
        pq.put((0, self.start))

        while not pq.empty():
            (dist, current_vertex) = pq.get()
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
                            self.parent[neighbor]=current_vertex


        return D


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
start = input('Enter Start Point: ')
end = input('Enter End Point: ')

D = g.dijkstra(start, end)
g.printSolution(D, g.parent)
print()

for i in range(len(g.edges)):
    position = -1
    for j in g.edges[i]:
        position += 1
        if j > 0:
            print (i,' has edge to', position)
# {0: 0, 1: 4, 2: 11, 3: 17, 4: 9, 5: 22, 6: 7, 7: 8, 8: 11}
print()
for vertex in range(len(D)):
    print("Distance from vertex ", start, " to vertex", vertex, "is", D[vertex])