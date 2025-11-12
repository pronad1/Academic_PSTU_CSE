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
    Depth-Limited DFS (used inside Iterative Deepening)
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

    # goal not found within this depth
    return None


def iterative_deepening_dfs(start, goal, max_depth):
    """
    Iterative Deepening DFS:
    Repeatedly calls dfs_limited with depth = 0, 1, 2, ..., max_depth
    Returns the first path found.
    """
    for depth in range(max_depth + 1):
        # print(f"Trying depth limit = {depth}")  # (optional debug)
        path = dfs_limited(start, goal, depth)
        if path is not None:
            return path    # found a path at this depth

    return None  # no path found up to max_depth


# ---- Example run ----
start = 'A'
goal = 'F'
max_depth = 4   # you can change this

path = iterative_deepening_dfs(start, goal, max_depth)
print(f"Iterative Deepening DFS from {start} to {goal} => {path}")
