from queueADT import Queue

def dijkstra(graph, start_vertex, end_vertex):
    graph.end = int(end_vertex)
    graph.start = int(start_vertex)
    D = {v: float('inf') for v in range(graph.v)}
    D[graph.start] = 0
    graph.parent = {v: int(-1) for v in range(graph.v)}
    pq = Queue()
    pq.enqueue((0, graph.start))
    graph.visited.clear()
    while not pq.isEmpty():
        (temp, current_vertex) = pq.dequeue()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.enqueue((new_cost, neighbor))
                        D[neighbor] = new_cost
                        graph.parent[neighbor] = current_vertex

    return D
