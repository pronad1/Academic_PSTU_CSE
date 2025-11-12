from collections import deque

# 🔹 Same built-in graph
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def bfs_shortest_path(start, goal):
    queue = deque([[start]])  # queue of paths
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path  # found shortest path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append(new_path)

    return None  # no path found


# ---- Example run ----
start = 'A'
goal = 'F'
path = bfs_shortest_path(start, goal)
print("Shortest path from", start, "to", goal, "=>", path)
