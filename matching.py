
from queueADT import Queue
from graphADT import g as graph



class NewBooking:

    def __init__(self, customerLocation, maxDist, CustomerName):
        self.customerLocation = customerLocation
        self.max = maxDist
        self.CustomerName = CustomerName
        self.driverName = None
        self.driverToCustomer = []

    def finddriver(self):
        driverisat = 'No driver'
        driverID = None

        if self.customerLocation in graph.driverLocation and len(graph.driverLocation[self.customerLocation]) > 0:  # if driver is at current location
                driverID = graph.driverLocation[self.customerLocation].pop(0)  # pop first driver at current location
                self.driverName = graph.drivers[driverID][0]
                return self.customerLocation, driverID, self.driverName
        visited = {}
        bfs_traversal_output = []
        queue = Queue()
        for location in graph.edgeGraph.keys():
            visited[location] = False
        visited[self.customerLocation] = True
        queue.enqueue(self.customerLocation)

        while not queue.isEmpty():
            u = queue.dequeue()
            bfs_traversal_output.append(u)
            for v in graph.edgeGraph[u]:
                if not visited[v[0]]:
                    if v[0] in graph.driverLocation and v[1] < self.max and len(graph.driverLocation[v[0]]) > 0:  # v[0] = current search location
                            driverID = graph.driverLocation[v[0]].pop(0)  # this will pop driverID then find details from driverID array
                            driverisat = v[0]
                            self.driverName = graph.drivers[driverID][0]
                            return driverisat, driverID, self.driverName

                    visited[v[0]] = True
                    queue.enqueue(v[0])
                    # for j in graph.vertices.keys():

        return driverisat, driverID, self.driverName
