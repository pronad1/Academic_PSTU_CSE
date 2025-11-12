import random

# Objective function
def objective_function(x):
    return -x**2 + 10*x

# Generate neighbors for a state
def get_neighbors(x, step_size=1.0, count=5):
    neighbors = []
    for _ in range(count):
        step = random.uniform(-step_size, step_size)
        neighbors.append(x + step)
    return neighbors

# Local Beam Search
def local_beam_search(k, iterations):
    # Initialize k random solutions
    current_states = [random.uniform(0, 10) for _ in range(k)]
    
    for i in range(iterations):
        all_neighbors = []
        
        # Generate neighbors for all states
        for state in current_states:
            neighbors = get_neighbors(state)
            all_neighbors.extend(neighbors)
        
        # Combine current states and neighbors
        combined = current_states + all_neighbors
        
        # Sort by objective function (descending order)
        combined.sort(key=objective_function, reverse=True)
        
        # Keep the top k states
        current_states = combined[:k]

    # Return the best solution
    best_state = max(current_states, key=objective_function)
    return best_state, objective_function(best_state)

# Run the algorithm
best_solution, best_value = local_beam_search(k=3, iterations=100)
print(f"Best solution found: x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")
