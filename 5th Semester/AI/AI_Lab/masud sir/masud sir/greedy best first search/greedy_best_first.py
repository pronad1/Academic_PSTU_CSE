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

# 🔹 Heuristic values h(n) (just an example)
#    Smaller = "closer" to goal (F)
h = {
    'A': 3,
    'B': 2,
    'C': 1,
    'D': 3,
    'E': 2,
    'F': 0
}

def greedy_best_first_search(start, goal):
    """
    Greedy Best-First Search:
    Chooses next node based ONLY on heuristic h(n)
    (does NOT guarantee shortest path)
    """

    # priority queue stores: (h(node), path)
    pq = []
    heapq.heappush(pq, (h[start], [start]))

    visited = set()

    while pq:
        _, path = heapq.heappop(pq)
        node = path[-1]

        if node == goal:
            return path

        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                new_path = path + [neighbor]
                heapq.heappush(pq, (h[neighbor], new_path))

    return None  # no path found


# ---- Example run ----
start = 'A'
goal = 'F'
path = greedy_best_first_search(start, goal)
print("Greedy Best-First Search path from", start, "to", goal, "=>", path)
