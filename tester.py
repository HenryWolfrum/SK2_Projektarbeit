import fitness_evaluator
import maze_generator
import maze_renderer
import population_manager
import population_analyzer
import maze_data_storage
import time
import algorithm_comparer as ac
import multiprocessing
import os

class Tester:

    def __init__(self):
        self.maze_generator = maze_generator.MazeGenerator()
        self.maze_renderer = maze_renderer.MazeRenderer()
        self.fitness_evaluator = fitness_evaluator.FitnessEvaluator()
        self.maze_data_storage = maze_data_storage.MazeDataStorage()


    def createRandomMaze(self):
        start=time.time()
        maze_obj = self.maze_generator.generateMaze(25,"RANDOM")
        end=time.time()
        print("\n"+str(end-start)+"\n")

        self.maze_renderer.renderPathInMaze(maze_obj,maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")

        print("\n\nFitness:", fitness)

        self.ask_for_save(maze_obj)

    def createRandomDFSMaze(self):
        start=time.time()
        maze_obj = self.maze_generator.generateMaze(25, "RANDOM_DFS")
        end=time.time()
        print("\n"+str(end-start)+"\n")
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

        log_info = input("Fortschritt anzeigen? (j/n): ").strip().lower()

        while log_info !="j" and log_info != "n":
            log_info = input("Fortschritt anzeigen? (j/n): ").strip().lower()

        if log_info == "j":
            log_info=True
        else:
            log_info=False

        maze_obj = self.maze_generator.geneticAlgorithmMaze(25,"RANDOM",pop_size,"IMPROVED",hyperparams,generations,log_info,"REDUCED")

        self.maze_renderer.renderPathInMaze(maze_obj, maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj, "IMPROVED")

        print("\n\nFitness:", fitness)

        self.ask_for_save(maze_obj)



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

        log_info = input("Fortschritt anzeigen? (j/n): ").strip().lower()

        while log_info != "j" and log_info != "n":
            log_info = input("Fortschritt anzeigen? (j/n): ").strip().lower()

        if log_info == "j":
            log_info = True
        else:
            log_info = False

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
        print("\n[INFO] Starte Algorithmusauswahl...")

        compare_set = []


        comparer = ac.AlgorithmComparer(200,100)


        tasks = comparer.build_tasks(experiment_runs=30)

        print(f"\n[INFO] Starte {len(tasks)} Tasks auf {max(1, os.cpu_count() - 1)} Kernen...")
        print("[INFO] Geschätzte Zeit")
        with multiprocessing.Pool(processes=max(1, os.cpu_count() - 1)) as pool:
            raw_results = pool.starmap(ac._evaluate_worker_batch, tasks)

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


    def ask_for_save(self,maze_obj):
        save_ask = input("\nLabyrinth Speichern? (j/n): ").strip().lower()
        if save_ask == "j":
            maze_id = input("\nSpeichername eingeben:")

            self.maze_data_storage.save_maze_data(maze_obj, maze_id)

    def choose_comparsion_set(self):
        compare_set = set()
        query = input("\n Wähle einen Algorithmustyp zum hinzufügen: [RANDOM] (R), [RANDOM_DFS] (D), [GENETIC_ALGORITHM] (G)").strip().upper()

        while query not in ["R", "D", "G"]:
            query = input(
                "\n Wähle einen Algorithmustyp zum hinzufügen: [RANDOM] (R), [RANDOM_DFS] (D), [GENETIC_ALGORITHM] (G)").strip().upper()

        compare_set.add(query)
