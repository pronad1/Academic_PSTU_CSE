import random

# Objective function
def objective_function(x):
    return -x**2 + 10*x  # Target is to maximize this

# Create an individual
def create_individual():
    return random.uniform(0, 10)  # Random value between 0 and 10

# Create initial population
def create_population(size=10):
    return [create_individual() for _ in range(size)]

# Selection - choose best individuals
def selection(population, fitness, retain=0.5):
    # Pair each individual with fitness
    graded = [(individual, fitness(individual)) for individual in population]
    # Sort by fitness (high to low)
    graded = sorted(graded, key=lambda x: x[1], reverse=True)
    # Select top individuals
    retain_length = int(len(graded) * retain)
    selected = [x[0] for x in graded[:retain_length]]
    return selected

# Crossover - combine two parents to create a child
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2  # Simple average

# Mutation - random small change
def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        return individual + random.uniform(-1, 1)
    return individual

# Genetic Algorithm
def genetic_algorithm(generations=50, population_size=10):
    population = create_population(population_size)

    for generation in range(generations):
        # Selection
        selected = selection(population, objective_function)
        
        # Create next generation
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)
        
        population = next_generation

    # Return best solution
    best = max(population, key=objective_function)
    return best, objective_function(best)

# Run the algorithm
best_solution, best_value = genetic_algorithm()
print(f"Best solution found: x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")
