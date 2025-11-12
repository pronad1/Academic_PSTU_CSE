from collections import deque

# 🔹 Built-in graph (same style as before)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def build_reverse_graph(graph):
    """Create reverse adjacency list for searching backwards from goal."""
    rev = {node: [] for node in graph}
    for u in graph:
        for v in graph[u]:
            if v not in rev:
                rev[v] = []
            rev[v].append(u)
    return rev


def reconstruct_path(meet, front_parent, back_parent):
    """Rebuild full path from start -> meet -> goal."""
    # from start to meet
    path_front = []
    node = meet
    while node is not None:
        path_front.append(node)
        node = front_parent.get(node)
    path_front.reverse()   # now start -> ... -> meet

    # from meet to goal
    path_back = []
    node = back_parent.get(meet)
    while node is not None:
        path_back.append(node)
        node = back_parent.get(node)

    # combine
    return path_front + path_back


def bidirectional_search(start, goal):
    if start == goal:
        return [start]

    # forward and backward visited sets
    front_visited = {start}
    back_visited = {goal}

    front_parent = {start: None}
    back_parent = {goal: None}

    # queues for BFS from both ends
    front_queue = deque([start])
    back_queue = deque([goal])

    # reverse graph for backward search
    rev_graph = build_reverse_graph(graph)

    while front_queue and back_queue:
        # ---- expand one step from the front side ----
        for _ in range(len(front_queue)):
            current = front_queue.popleft()

            for neighbor in graph.get(current, []):
                if neighbor not in front_visited:
                    front_visited.add(neighbor)
                    front_parent[neighbor] = current
                    front_queue.append(neighbor)

                    # check if this node was reached from the other side
                    if neighbor in back_visited:
                        return reconstruct_path(neighbor, front_parent, back_parent)

        # ---- expand one step from the back side ----
        for _ in range(len(back_queue)):
            current = back_queue.popleft()

            for neighbor in rev_graph.get(current, []):
                if neighbor not in back_visited:
                    back_visited.add(neighbor)
                    back_parent[neighbor] = current
                    back_queue.append(neighbor)

                    # check meeting
                    if neighbor in front_visited:
                        return reconstruct_path(neighbor, front_parent, back_parent)

    # no connection
    return None


# ---- Example run ----
start = 'A'
goal = 'F'
path = bidirectional_search(start, goal)
print("Bidirectional Search path from", start, "to", goal, "=>", path)
