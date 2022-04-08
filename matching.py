import customer
import driver
from queueADT import Queue
from graphADT import g
# from main2 import customer, driver, graph
class newBooking:

    # def __init__(self):
        # self.customer = customer
        # self.driver = None
        # self.success = False
        # self.drivertoCustomer = []

    def finddriver(self, graph, s, max):
        print('I am ran')
        driverisat = 'No driver'
        driverID = None

        if s in graph.driverLocation:  # if driver is at current location
            driverID = graph.driverLocation[s].pop(0)  # pop first driver at current location
            return s, driverID
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
                    if v[0] in graph.driverLocation and v[1]< max: # v[0] = current search location
                        driverID = graph.driverLocation[v[0]].pop(0) # this will pop driverID then find details from driverID array
                        driverisat=v[0]
                        return driverisat, driverID

                    visited[v[0]] = True
                    queue.enqueue(v[0])
                    # for j in graph.vertices.keys():

        return driverisat, driverID
testbooking = newBooking()
driverStart, driveridd = testbooking.finddriver(g, 1, 200)

if driverStart != 'No driver':
    print('Driver is at', int(driverStart))

else:
    print('No driver nearby! ')






