from queue import PriorityQueue

def dijkstra(graph, startLoc, endLoc):
    # setting graph start to starting location
    graph.start = int(startLoc)
    # setting graph end to end location
    graph.end = int(endLoc)
    # initialising all distance to location as Infinity for comparison
    distTo = {v: float('inf') for v in range(graph.v)}
    # Distance from start to start is set to 0
    distTo[graph.start] = 0
    # initialising parent to keep track of path taken
    graph.parent = {v: int(-1) for v in range(graph.v)}
    # initialising queueADT to keep track of cost and neighbour
    pQ = PriorityQueue()
    pQ.put((0, graph.start))
    graph.visited.clear()
    # Run while there are still locations in queue
    while not pQ.empty():
        (temp, current_vertex) = pQ.get()
        # Adding vertex to visited
        graph.visited.append(current_vertex)
        # visiting neighbour of current vertex
        for neighbor in range(graph.v):
            # if distance is not negative
            if graph.edges[current_vertex][neighbor] != -1:
                # set distance to current distance from neighbour to current vertex
                distance = graph.edges[current_vertex][neighbor]
                # if neighbour has not been visited
                if neighbor not in graph.visited:
                    # Compare new and old distance, if new distance is shorter, update parent and distTo
                    old_cost = distTo[neighbor]
                    new_cost = distTo[current_vertex] + distance
                    if new_cost < old_cost:
                        pQ.put((new_cost, neighbor))
                        distTo[neighbor] = new_cost
                        graph.parent[neighbor] = current_vertex
    # Return distTo for finding path
    return distTo
