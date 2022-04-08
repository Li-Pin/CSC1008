import customer
import driver
class newBooking:
    def __init__(self, customer):
        self.customer = customer
        self.driver = None
        self.success = False
        self.drivertoCustomer = []

def finddriver(graph, s, max):

    driverisat = 'No driver'
    if graph.locations[s][3]==True:
        driverisat=s
        return driverisat
    print('ran false')
    visited = {}
    bfs_traversal_output = []
    queue = Queue()
    for location in graph.edgeGraph.keys():
        visited[location] = False
    visited[s] = True
    queue.enqueue(s)

    while not queue.isEmpty():
        u = queue.dequeue()
        bfs_traversal_output.append(u)
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

    print(bfs_traversal_output)
    return driverisat

def bookRide(self, start, end):
    self.dist = start + end

    self.dist = g.dijkstra(start, end)

driverStart = finddriver(g, int(start), int(max))

if driverStart != 'No driver':
    print('Driver is at', int(driverStart))
    C = g.dijkstra(str(driverStart), start)
    g.printSolution(C, g.parent, driverPath)
else:
    print('No driver nearby! ')