import random

def count_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:  # Same row
                conflicts += 1
            if abs(state[i] - state[j]) == abs(i - j):  # Diagonal
                conflicts += 1
    return conflicts

def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                new_state = list(state)
                new_state[col] = row
                neighbors.append(tuple(new_state))
    return neighbors

def local_beam_search(n=8, k=4, max_iter=200):
    states = [tuple(random.randint(0, n-1) for _ in range(n)) for _ in range(k)]
    
    print(f"Starting with {k} random states\n")
    
    for iteration in range(max_iter):
        # Step 2: Check if goal found
        for state in states:
            if count_conflicts(state) == 0:
                print(f"✓ Solution found at iteration {iteration}!")
                return state, iteration
        
        # Step 3: Generate all successors
        all_successors = []
        for state in states:
            all_successors.extend(get_neighbors(state))
        
        # Step 4: Select k best successors
        all_successors.sort(key=count_conflicts)
        states = all_successors[:k]
        
        # Progress update
        if (iteration + 1) % 50 == 0:
            print(f"Iteration {iteration + 1}: Best conflicts = {count_conflicts(states[0])}")
    
    # Return best state found
    best = min(states, key=count_conflicts)
    print(f"\nBest state found with {count_conflicts(best)} conflicts")
    return best, max_iter


# Main Program
if __name__ == "__main__":
    print("="*50)
    print("LOCAL BEAM SEARCH - 8 Queens Problem")
    print("="*50 + "\n")
    
    solution, iters = local_beam_search(n=8, k=4, max_iter=200)
    
    print("\n" + "="*50)
    print("RESULT")
    print("="*50)
    
    if count_conflicts(solution) == 0:
        print(f"Solution: {solution}")
        print("\nBoard:")
        for row in range(8):
            print("  " + " ".join("Q" if solution[col] == row else "." for col in range(8)))
    else:
        print(f"Best: {solution}")
        print(f"Conflicts: {count_conflicts(solution)}")
        print("Try increasing k or max_iter!")
