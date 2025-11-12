import heapq

# 🔹 Same built-in graph
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# 🔹 Heuristic values h(n) (example for goal = 'F')
#    Smaller = "closer" to goal
h = {
    'A': 3,
    'B': 2,
    'C': 1,
    'D': 3,
    'E': 2,
    'F': 0
}

def a_star_search(start, goal):
    """
    A* Search:
    f(n) = g(n) + h(n)
    g(n) = cost so far (here: number of steps)
    h(n) = heuristic estimate to goal
    """

    # priority queue stores: (f, g, node, path)
    pq = []
    heapq.heappush(pq, (h[start], 0, start, [start]))

    # best known g(n) for each node
    g_score = {start: 0}

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node == goal:
            return path, g  # path and total cost

        # If we already found a better path to this node, skip
        if g > g_score.get(node, float('inf')):
            continue

        for neighbor in graph.get(node, []):
            new_g = g + 1  # cost of edge = 1

            # If this path to neighbor is better, record it
            if new_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g
                new_f = new_g + h[neighbor]
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_f, new_g, neighbor, new_path))

    return None, float('inf')  # no path found


# ---- Example run ----
start = 'A'
goal = 'F'
path, cost = a_star_search(start, goal)
print("A* Search path from", start, "to", goal, "=>", path, "with cost", cost)
