from queueADT import Queue
from graphADT import g as graph


class NewBooking:
    # Constructor to match driver to new customer's booking
    def __init__(self, customerLocation, CustomerName):
        self.customerLocation = customerLocation
        self.CustomerName = CustomerName
        self.driverName = None
        self.driverToCustomer = []

    # Function called when customer create booking to find driver
    def finddriver(self):
        # Initialise to no driver at the beginning
        driverisat = 'No driver'
        driverID = None

        # If driver is at current location
        if self.customerLocation in graph.driverLocation and len(graph.driverLocation[self.customerLocation]) > 0:
            # This will pop first driver at current location
            driverID = graph.driverLocation[self.customerLocation].pop(0)
            self.driverName = graph.drivers[driverID][0]
            return self.customerLocation, driverID, self.driverName

        # To mark visited locations
        visited = {}
        # To transverse Breadth First Search outputs
        bfs_traversal_output = []
        # Using Queue ADT
        queue = Queue()

        # Set all visited location to false
        for location in graph.edgeGraph.keys():
            visited[location] = False

        # only set customer's location to true and add to queue
        visited[self.customerLocation] = True
        queue.enqueue(self.customerLocation)

        while not queue.isEmpty():
            u = queue.dequeue()
            bfs_traversal_output.append(u)
            for v in graph.edgeGraph[u]:
                # v[0] = current search location
                if not visited[v[0]]:
                    # check if current search location in driver's location area
                    if v[0] in graph.driverLocation and len(graph.driverLocation[v[0]]) > 0:
                        # this will pop driverID then find details from driverID array
                        driverID = graph.driverLocation[v[0]].pop(0)
                        # set driver location to current search location
                        driverisat = v[0]
                        self.driverName = graph.drivers[driverID][0]
                        return driverisat, driverID, self.driverName

                    # set current search location as visited
                    visited[v[0]] = True
                    # add it to queue to mark as visited
                    queue.enqueue(v[0])

        return driverisat, driverID, self.driverName
