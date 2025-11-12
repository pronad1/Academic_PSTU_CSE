import random


def objective_function(x):
    return -x**2 + 10*x

def get_neighbor(x):
    step = random.uniform(-1, 1)  # Small random step
    return x + step

def hill_climbing(iterations=1000):
    # Start with a random solution
    current_solution = random.uniform(0, 10)
    current_value = objective_function(current_solution)

    for i in range(iterations):
        neighbor = get_neighbor(current_solution)
        neighbor_value = objective_function(neighbor)

    
        if neighbor_value > current_value:
            current_solution = neighbor
            current_value = neighbor_value

    return current_solution, current_value


best_solution, best_value = hill_climbing()
print(f"Best solution found: x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")
