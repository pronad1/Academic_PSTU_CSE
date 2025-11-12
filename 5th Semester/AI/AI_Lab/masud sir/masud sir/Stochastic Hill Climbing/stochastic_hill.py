import random

def objective_function(x):
    # Same function as before: f(x) = -x^2 + 10x
    return -x**2 + 10*x

def get_neighbor(x):
    # Generate a random neighbor by a small step
    step = random.uniform(-1, 1)
    return x + step

def stochastic_hill_climbing(iterations=1000, neighbors_per_step=10):
    # Start with a random solution in [0, 10]
    current_solution = random.uniform(0, 10)
    current_value = objective_function(current_solution)

    for i in range(iterations):
        # Generate several random neighbors
        neighbors = [get_neighbor(current_solution) for _ in range(neighbors_per_step)]

        # Keep only neighbors that are better (uphill moves)
        better_neighbors = [n for n in neighbors if objective_function(n) > current_value]

        if better_neighbors:
            # Choose ONE random better neighbor (stochastic choice)
            new_solution = random.choice(better_neighbors)
            current_solution = new_solution
            current_value = objective_function(current_solution)
            # If you want to see progress, uncomment:
            # print(f"Iter {i}: x = {current_solution:.4f}, f(x) = {current_value:.4f}")
        # else:
            # No better neighbor found this step (could be local maximum / plateau)
            # In pure stochastic HC, we just stay and try again next iteration

    return current_solution, current_value


# ---- Example run ----
best_solution, best_value = stochastic_hill_climbing()
print(f"Best solution found: x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")
