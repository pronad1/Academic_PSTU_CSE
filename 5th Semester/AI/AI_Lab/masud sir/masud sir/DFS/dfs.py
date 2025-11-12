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

def dfs_path(start, goal):
    # stack will store paths (like BFS queue, but LIFO)
    stack = [[start]]
    visited = set([start])
    
    while stack:
        path = stack.pop()      # take the LAST path (LIFO)
        node = path[-1]
        
        if node == goal:
            return path         # found a path (NOT guaranteed shortest)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                stack.append(new_path)
    
    return None  # no path found


# ---- Example run ----
start = 'A'
goal = 'F'
path = dfs_path(start, goal)
print("DFS path from", start, "to", goal, "=>", path)
