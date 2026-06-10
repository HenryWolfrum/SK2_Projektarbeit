import maze_generator

# Die Arbeitsfunktion für den einzelnen Kern
#Evaluiert exakt eine Konfiguration
def evaluate_single_run(setting):
    mutation_rate, survivor_rate, tournament_size, run_idx = setting

    hyper_dict = {
        "mutation_rate": mutation_rate,
        "survivor_rate": survivor_rate,
        "tournament_size": tournament_size
    }

    m_g = maze_generator.MazeGenerator()

    # Führt exakt einen Durchlauf aus
    maze = m_g.geneticAlgorithmMaze(25, "RANDOM", 100, "IMPROVED", hyper_dict, 200)

    #Ergbenis dictionary
    return {
        "mutation_rate": mutation_rate,
        "survivor_rate": survivor_rate,
        "tournament_size": tournament_size,
        "fitness": maze.fitness
    }

