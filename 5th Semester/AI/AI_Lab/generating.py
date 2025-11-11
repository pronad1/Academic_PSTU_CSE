import math
import random

def simulated_annealing(objective_function, initial_solution, neighbor_function,
                        T=1000, cooling_rate=0.995, stopping_T=1e-6, max_iter=100000):
    """
    Generic Simulated Annealing Algorithm.

    Parameters:
    - objective_function: function to minimize (takes a solution, returns cost)
    - initial_solution: starting point (list, tuple, or custom representation)
    - neighbor_function: function that generates a neighbor solution
    - T: initial temperature
    - cooling_rate: rate of cooling (0 < cooling_rate < 1)
    - stopping_T: final temperature
    - max_iter: maximum number of iterations

    Returns:
    - best_solution: the best solution found
    - best_cost: the cost of the best solution
    """

    # Start with the initial solution
    current_solution = initial_solution
    current_cost = objective_function(current_solution)

    best_solution = current_solution
    best_cost = current_cost

    iteration = 1
    while T > stopping_T and iteration < max_iter:
        # Generate a neighbor solution
        new_solution = neighbor_function(current_solution)
        new_cost = objective_function(new_solution)

        # Accept better solutions, or worse with probability
        if new_cost < current_cost:
            current_solution, current_cost = new_solution, new_cost
        else:
            if random.random() < math.exp(-(new_cost - current_cost) / T):
                current_solution, current_cost = new_solution, new_cost

        # Update best found
        if current_cost < best_cost:
            best_solution, best_cost = current_solution, current_cost

        # Cooling step
        T *= cooling_rate
        iteration += 1

    return best_solution, best_cost

# Objective function
def f(x):
    return x**2 + 10*math.sin(x)

# Initial solution
initial_solution = random.uniform(-10, 10)

# Neighbor: small random change
def neighbor(x):
    return x + random.uniform(-1, 1)

best, cost = simulated_annealing(f, initial_solution, neighbor)
print("Best solution (x):", best)
print("Best cost f(x):", cost)
