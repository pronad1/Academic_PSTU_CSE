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

def dfs_limited(start, goal, limit):
    """
    Depth-Limited DFS
    start : starting node
    goal  : goal node
    limit : maximum depth allowed (0 = only start node)
    """
    # stack stores: (current_node, path_so_far, current_depth)
    stack = [(start, [start], 0)]

    while stack:
        node, path, depth = stack.pop()

        # goal test
        if node == goal:
            return path

        # only expand if we are below depth limit
        if depth < limit:
            for neighbor in graph.get(node, []):
                new_path = path + [neighbor]
                stack.append((neighbor, new_path, depth + 1))

    # if goal not found within depth limit
    return None


# ---- Example run ----
start = 'A'
goal = 'F'

limit = 2   # try changing this to 1 or 3 and see the difference

path = dfs_limited(start, goal, limit)
print(f"Depth-limited DFS (limit = {limit}) from {start} to {goal} => {path}")
