import itertools
import multiprocessing
import os
import json
import numpy as np

import maze_generator

# Die Arbeitsfunktion für den einzelnen Kern (muss frei ganz oben stehen)
def evaluate_single_run(setting):
    mutation_rate, survivor_rate, tournament_size, run_idx = setting

    hyper_dict = {
        "mutation_rate": mutation_rate,
        "survivor_rate": survivor_rate,
        "tournament_size": tournament_size
    }

    m_g = maze_generator.MazeGenerator()

    # Führt exakt einen Durchlauf aus (200 Gen)
    maze = m_g.geneticAlgorithmMaze(25, "RANDOM", 100, "IMPROVED", hyper_dict, 200)

    return {
        "mutation_rate": mutation_rate,
        "survivor_rate": survivor_rate,
        "tournament_size": tournament_size,
        "fitness": maze.fitness
    }


if __name__ == '__main__':
    # Alle Kerne bis auf einen aktivieren
    cores_to_use = max(1, os.cpu_count() - 1)

    #Suchräume
    mutation_space = [0.02, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5]
    survivor_space = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.7]
    tournament_space = [2, 3, 5, 8]
    runs = range(5)

    # Erzeugt Kreuzprodukt über Suchräume
    task_packages = list(itertools.product(mutation_space, survivor_space, tournament_space, runs))


    # Parallelisierung
    with multiprocessing.Pool(processes=cores_to_use) as pool:
        raw_results = pool.map(evaluate_single_run, task_packages)


    # Statistiken berechnen
    aggregated_data = {}
    for res in raw_results:
        #Schlüssel ist eindeutiges Hyperparameter Tupel
        key = (res["mutation_rate"], res["survivor_rate"], res["tournament_size"])
        if key not in aggregated_data:
            aggregated_data[key] = []
        aggregated_data[key].append(res["fitness"])

    # Ergebnisliste für JSON
    final_grid_results = []
    for (mutation_rate, survivor_rate, tournament_size), fitness_list in aggregated_data.items():
        final_grid_results.append({
            "mutation_rate": mutation_rate,
            "survivor_rate": survivor_rate,
            "tournament_size": tournament_size,
            "fitness": float(np.mean(fitness_list)),
            "standard_deviation": float(np.std(fitness_list)),
            "max_fitness": float(np.max(fitness_list))
        })

    # Ergebnisse als JSON speichern
    with open("hyperparameter_tuning_results.json", "w") as f:
        json.dump(final_grid_results, f, indent=4)

    print("Alles erledigt! Die Daten liegen sicher in 'hyperparameter_tuning_results.json'.")