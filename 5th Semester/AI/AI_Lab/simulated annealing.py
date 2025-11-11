import math
import random
import matplotlib.pyplot as plt


# -------------------------
# Distance Function
# -------------------------
def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


# -------------------------
# Evaluate Route
# -------------------------
def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # return to start
    return total


# -------------------------
# Simulated Annealing Algorithm
# -------------------------
def simulated_annealing(coord, T=1000, cooling_rate=0.995, stopping_T=1e-6, max_iter=100000):
    # Initial random route
    current_route = list(coord.keys())
    random.shuffle(current_route)
    current_distance = evalua_ruta(current_route, coord)

    best_route = current_route[:]
    best_distance = current_distance

    iteration = 1
    while T > stopping_T and iteration < max_iter:
        # Generate a neighbor (swap two cities)
        new_route = current_route[:]
        i, j = random.sample(range(len(new_route)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]

        new_distance = evalua_ruta(new_route, coord)

        # Check acceptance
        if new_distance < current_distance:
            current_route, current_distance = new_route, new_distance
        else:
            # Accept worse solution with probability
            if random.random() < math.exp(-(new_distance - current_distance) / T):
                current_route, current_distance = new_route, new_distance

        # Track best solution
        if current_distance < best_distance:
            best_route, best_distance = current_route[:], current_distance

        # Cooling
        T *= cooling_rate
        iteration += 1

    return best_route, best_distance


# -------------------------
# Plotting Function
# -------------------------
def plot_route(ruta, coord, title="Route Visualization"):
    plt.figure(figsize=(8, 6))

    x = [coord[city][1] for city in ruta] + [coord[ruta[0]][1]]
    y = [coord[city][0] for city in ruta] + [coord[ruta[0]][0]]

    plt.plot(x, y, '-o', color="red", linewidth=2, markersize=8)

    for city in ruta:
        plt.text(coord[city][1] + 0.1, coord[city][0] + 0.1, city, fontsize=9)

    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.show()


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    coord = {
        'JiloYork': (19.984146, -99.519127),
        'Toluca': (19.286167856525594, -99.65473296644892),
        'Atlacomulco': (19.796802401380955, -99.87643301629244),
        'Guadalajara': (20.655773344775373, -103.35773871581326),
        'Monterrey': (25.675859554333684, -100.31405053526082),
        'Cancún': (21.158135651777727, -86.85092947858692),
        'Morelia': (19.720961251258654, -101.15929186858635),
        'Aguascalientes': (21.88473831747085, -102.29198705069501),
        'Queretaro': (20.57005870003398, -100.45222862892079),
        'CDMX': (19.429550164848152, -99.13000959477478)
    }

    best_route, best_distance = simulated_annealing(coord)
    print("Best Route:", best_route)
    print("Total Distance:", best_distance)

    # Plot best solution
    plot_route(best_route, coord, title="Best Route Found by Simulated Annealing")
