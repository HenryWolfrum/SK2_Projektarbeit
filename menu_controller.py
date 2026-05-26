import fitness_evaluator
import maze_generator
import maze_renderer
import population_manager
import population_analyzer
import maze_data_storage
import algorithm_comparer as ac
import multiprocessing
import itertools
import environment
import agent
import os
import hyperparameter_result_plotter
import hyperparameter_tuner
import numpy as np
import json

class MenuController:

    def __init__(self):
        self.maze_generator = maze_generator.MazeGenerator()
        self.maze_renderer = maze_renderer.MazeRenderer()
        self.fitness_evaluator = fitness_evaluator.FitnessEvaluator()
        self.maze_data_storage = maze_data_storage.MazeDataStorage()

    def _ask_yes_no(self, prompt):
        answer = input(prompt).strip().lower()
        while answer not in ["j", "n"]:
            answer = input(prompt).strip().lower()
        return answer

    def createRandomMaze(self):

        maze_obj = self.maze_generator.generateMaze(25,"RANDOM")

        self.maze_renderer.renderPathInMaze(maze_obj,maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")

        print("\n\nFitness:", fitness)

        self.ask_for_save(maze_obj)

    def createRandomDFSMaze(self):

        maze_obj = self.maze_generator.generateMaze(25, "RANDOM_DFS")

        self.maze_renderer.renderPathInMaze(maze_obj, maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")

        print("\n\nFitness:", fitness)

        self.ask_for_save(maze_obj)

    def createGAMaze(self):
        pop_size = int(input("Populationsgröße:"))
        mutation_rate = float(input("Mutations Rate:"))
        survivor_rate = float(input("Überlebenden Rate:"))
        tournament_size = int(input("Turniergröße:"))
        generations = int(input("Generationendurchläufe:"))

        hyperparams = {"mutation_rate":mutation_rate,
                       "survivor_rate":survivor_rate,
                       "tournament_size":tournament_size}

        log_info = self._ask_yes_no("Fortschritt anzeigen? (j/n): ") == "j"

        maze_obj = self.maze_generator.geneticAlgorithmMaze(25,"RANDOM",pop_size,"IMPROVED",hyperparams,generations,log_info,"REDUCED")

        self.maze_renderer.renderPathInMaze(maze_obj, maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")

        print("\n\nFitness:", fitness)

        self.ask_for_save(maze_obj)


    def agent_game(self):
        print("\n[INFO] Spielumgebung laden...")

        name = input("Wähle Labyrinth auf dem gespielt werden soll: ")

        maze_obj = self.maze_data_storage.load_maze_data(name)

        if maze_obj is None:
            print("\n[INFO] Labyrinth wurde nicht gefunden!")
            input("\n Drücke ENTER um fortzufahren...")
            return

        coin_count = int(input("\n Wähle Anzahl an zu suchenden Münzen:"))

        print("\n[INFO] Simuliere Spiel...")
        ag = agent.GreedyAgent()
        env = environment.Environment(maze_obj,ag)

        #Spiel wird gestartet
        env.start(coin_count)

        print("\n[INFO] Spiel fertig simuliert!")

        env.evaluateSolution()


        input("\n[INFO] Drücke ENTER um fortzufahren...")


    #Ertellt eine Beispiel Population und wertet die Daten aus
    def createPopulation(self):
        #Analyse-Beobachter erstellen
        analyzer = population_analyzer.PopulationAnalyzer()

        #Populationsparameter abfragen
        pop_size = int(input("Populationsgröße:"))
        mutation_rate = float(input("Mutations Rate:"))
        survivor_rate = float(input("Überlebenden Rate:"))
        tournament_size = int(input("Turniergröße:"))
        generations = int(input("Generationendurchläufe:"))

        hyperparams = {"mutation_rate": mutation_rate,
                       "survivor_rate": survivor_rate,
                       "tournament_size": tournament_size}

        log_info = self._ask_yes_no("Fortschritt anzeigen? (j/n): ") == "j"

        #Eine Population erstellen
        pop = population_manager.PopulationManager(25,"RANDOM",pop_size,"IMPROVED",hyperparams,log_info,"FULL")

        #Analyse-Beobachter als Beobachter für Populationsverwalter hinzufügen
        pop.addObserver(analyzer)
        #Population evolvieren
        pop.runPopulation(generations)

        print("\n[INFO] Population wurde erfolgreich simuliert!")
        print("=" * 30 + "\n")
        print("\n[INFO] Lade fittestes Individuum...")
        maze_obj = analyzer.get_fittest_maze()
        self.maze_renderer.renderPathInMaze(maze_obj,maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")

        print("\n\nFitness:", fitness)

        self.ask_for_save(maze_obj)

        print("=" * 30 + "\n")
        print("\n [INFO] Lade Fitnesskonvergenz-Verlauf...")
        analyzer.plot_fitness_convergence()
        print("=" * 30 + "\n")
        print("\n [INFO] Lade Diversitäts-Verlauf...")
        analyzer.plot_diversity()
        print("=" * 30 + "\n")

    def compare_algorithms(self):
        print("\n=== Algorithmen vergleichen ===")
        print("\n[INFO] Starte Algorithmenauswahl...")

        compare_set = self.choose_compare_set()

        if len(compare_set) == 0:
            return

        comparer = ac.AlgorithmComparer(compare_set)

        experiment_runs = int(input("\nAnzahl unabhängiger Durchläufe: "))

        tasks = comparer.build_tasks(experiment_runs=experiment_runs)

        budget = comparer.evaluation_budget
        per_gen_estimate = 0.33
        per_random_estimate = 0.0122
        per_random_dfs_estimate = 0.0228
        total = 0

        for algo in compare_set:
            if algo[0] == "R":
                total += budget * per_random_estimate

            elif algo[0] == "D":
                total += budget * per_random_dfs_estimate

            else:
                total += (
                        (budget // algo[len(algo) - 1]) *
                        (algo[3] * per_gen_estimate)
                )

        total *= experiment_runs

        cores = max(1, os.cpu_count() - 1)

        print(f"\n[INFO] Geschätzte Zeit für Berechnung auf {cores} Kernen:")
        print(f"\n {total / cores:.2f} Sekunden")

        if self._ask_yes_no("Vergleichsberechnung durchführen? (j/n): ") == "n":
            return

        print(
            f"\n[INFO] Starte {len(tasks)} Tasks auf "
            f"{max(1, os.cpu_count() - 1)} Kernen..."
        )


        with multiprocessing.Pool(
                processes=max(1, os.cpu_count() - 1)
        ) as pool:
            raw_results = pool.starmap(
                ac._evaluate_worker_batch,
                tasks
            )


        compare_data = comparer.aggregate_results(raw_results)
        comparer.plot_results(compare_data)

    def load_maze(self):
        print("\n=== Labyrinth Laden ===")
        name = input("Bitte den Namen des Labyrinths eingeben: ")

        maze_obj = self.maze_data_storage.load_maze_data(name)

        if maze_obj is None:
            print("\n[INFO] Labyrinth wurde nicht gefunden!")
            return

        self.maze_renderer.renderPathInMaze(maze_obj, maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")
        print("\n")
        print("-" * 30)
        print(f"Fitness-Wert: {fitness}")
        print("=" * 30 + "\n")

    def list_maze_storage(self):
        print("\n=== Speicher Laden ===")
        self.maze_data_storage.list_data_names()
        print("=" * 25 + "\n")

    def delete_maze(self):
        print("\n=== Labyrinth Löschen ===")
        name = input("Name des zu löschenden Labyrinths: ")
        if self.maze_data_storage.delete_maze_data(name):
            print("\n[INFO] Löschen wurde erfolgreich durchgeführt!")
        else:
            print("\n[INFO] Labyrinth wurde nicht gefunden!")
        print("=" * 25 + "\n")

    def ask_for_save(self, maze_obj):
        if self._ask_yes_no("\nLabyrinth Speichern? (j/n): ") == "j":
            maze_id = input("\nSpeichername eingeben: ")
            self.maze_data_storage.save_maze_data(maze_obj, maze_id)

    def choose_compare_set(self):

        compare_set = []

        while True:

            query = input(
                "\n Wähle einen Algorithmustyp zum hinzufügen: "
                "[RANDOM] (R), [RANDOM_DFS] (D), "
                "[GENETIC_ALGORITHM] (G): "
            ).strip().upper()

            # Eingabe validieren
            while query not in ["R", "D", "G"]:
                query = input(
                    "\n Ungültige Eingabe! Wähle: "
                    "[RANDOM] (R), [RANDOM_DFS] (D), "
                    "[GENETIC_ALGORITHM] (G): "
                ).strip().upper()

            # RANDOM
            if query == "R":

                if any(x[0] == "R" for x in compare_set):
                    print("\n[INFO] RANDOM ist bereits im Vergleichsset!")
                    continue

                tupel = ("R", 1)

            # RANDOM_DFS
            elif query == "D":

                if any(x[0] == "D" for x in compare_set):
                    print("\n[INFO] RANDOM_DFS ist bereits im Vergleichsset!")
                    continue

                tupel = ("D", 1)

            # GENETIC ALGORITHM
            else:

                tupel = self._addGA()

                if tupel in compare_set:
                    print(
                        "\n[INFO] Diese GA-Konfiguration "
                        "existiert bereits!"
                    )
                    continue

            # Hinzufügen
            compare_set.append(tupel)

            print("\n[INFO] Algorithmus erfolgreich hinzugefügt!")

            # Abbrechen?
            answer = self._ask_yes_no(
                "\nWeiteren Algorithmus hinzufügen? (j/n): "
            )

            if answer == "n":
                break

        print("\n[INFO] Alle Algorithmen erfolgreich aufgenommen!")

        return compare_set

    def _addGA(self):
        popSize = int(input("Populationsgröße: "))
        mutation_rate = float(input("Mutations Rate: "))
        survivor_rate = float(input("Überlebenden Rate: "))
        tournament_size = int(input("Turniergröße: "))
        generations = int(input("Generationen: "))

        hyperparams = {
            "mutation_rate": mutation_rate,
            "survivor_rate": survivor_rate,
            "tournament_size": tournament_size
        }

        return "G", popSize, hyperparams, generations, (popSize * generations)


    def plot_tuning_results(self):
        answer = self._ask_yes_no("Ergebnisse mit Standardabweichung darstellen (j/n)? : ")
        print("\n[INFO] Ergebnisse der Hyperoptimierung werden geladen...")
        if answer == "n":
            hyperparameter_result_plotter.plot_tuning_results()
        else:
            hyperparameter_result_plotter.plot_tuning_results(True)




    def hyperparameter_tuning(self):

        print("\n [WARNUNG] Bei der Durchführung werden alte Ergebnisse überschrieben!")
        if self._ask_yes_no("\n Fortfahren? (j/n)") == "n":
            return

        print("\n[INFO] Suchräume definieren....")

        mutation_space = []
        survivor_space = []
        tournament_space = []

        len_mutation_space = int(input("Größe Mutationsraten-Suchraum:"))
        for _ in range(len_mutation_space):
            mutation_space.append(float(input("Mutations Rate " + str(_) + ": ")))

        len_survivor_space = int(input("Größe Überlebendenraten-Suchraum:"))
        for _ in range(len_survivor_space):
            survivor_space.append(float(input("Überlebenden Rate " + str(_) + ": ")))

        len_tournament_space = int(input("Größe Turniergrößen-Suchraum:"))
        for _ in range(len_tournament_space):
            tournament_space.append(int(input("Turniergröße " + str(_) + ": ")))  # FIX: int statt float

        runs = range(int(input("Simulierte Durchläufe pro Suchraum-Tupel: ")))

        # 0.33s pro Generation, 200 Generationen pro GA-Lauf
        per_ga_estimate = 0.33 * 200

        # Alle Kerne bis auf einen aktivieren
        cores = max(1, os.cpu_count() - 1)

        estimate_time = len(runs) * len_mutation_space * len_survivor_space * len_tournament_space * per_ga_estimate / cores

        print(f"\n[INFO] Die Berechnungen werden geschätzt {estimate_time / 60:.2f}min benötigen!")  # FIX: /3600 für Stunden
        if self._ask_yes_no("\n Fortfahren? (j/n)") == "n":
            return

        # Erzeugt Kreuzprodukt über Suchräume
        task_packages = list(itertools.product(mutation_space, survivor_space, tournament_space, runs))

        # Parallelisierung
        with multiprocessing.Pool(processes=cores) as pool:
            raw_results = pool.map(hyperparameter_tuner.evaluate_single_run, task_packages)

        # Statistiken berechnen
        aggregated_data = {}
        for res in raw_results:
            # Schlüssel ist eindeutiges Hyperparameter Tupel
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

        print("\n[INFO] Alle Berechnungen erfolgreich durchgeführt und gespeichert!")
        print("\n[INFO] Ergebnisse können jetzt geladen werden!")