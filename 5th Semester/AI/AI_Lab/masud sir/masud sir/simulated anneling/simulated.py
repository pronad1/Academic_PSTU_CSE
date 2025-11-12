import random
import math

def objective_function(x):
    return -x**2 + 10*x

def get_neighbor(x):
    return x + random.uniform(-1, 1)

def simulated_annealing(initial_temp=100, cooling_rate=0.95, iterations=1000):
    current_solution = random.uniform(0, 10)
    current_value = objective_function(current_solution)
    temperature = initial_temp
    
    best_solution = current_solution
    best_value = current_value

    for i in range(iterations):
        neighbor = get_neighbor(current_solution)
        neighbor_value = objective_function(neighbor)
        
        delta = neighbor_value - current_value
        
        if delta > 0:
            current_solution = neighbor
            current_value = neighbor_value
        else:
            probability = math.exp(delta / temperature)
            if random.random() < probability:
                current_solution = neighbor
                current_value = neighbor_value

        if current_value > best_value:
            best_solution = current_solution
            best_value = current_value

        temperature *= cooling_rate
        if temperature < 0.0001:
            break

    return best_solution, best_value

# Run SA
best_x_sa, best_fx_sa = simulated_annealing()
print("Simulated Annealing Result:")
print(f"x = {best_x_sa:.4f}, f(x) = {best_fx_sa:.4f}")
