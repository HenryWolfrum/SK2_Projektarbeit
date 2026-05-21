import fitness_evaluator
import maze_generator
import maze_renderer
import population_manager
import population_analyzer
import algorithm_comparer
import maze_data_storage

class Tester:

    def __init__(self):
        self.maze_generator = maze_generator.MazeGenerator()
        self.maze_renderer = maze_renderer.MazeRenderer()
        self.fitness_evaluator = fitness_evaluator.FitnessEvaluator()
        self.maze_data_storage = maze_data_storage.MazeDataStorage()


    #Erstellt ein Beispiel Labyrinth und zeichnet es mit Lösungspfad
    def createMaze(self,size=25,mode="RANDOM"):
        #Labyrinth generieren
        maze_obj=self.maze_generator.generateMaze(size,mode)

        #Labyrinth visualisieren mit Pfad
        self.maze_renderer.renderPathInMaze(maze_obj,maze_obj.solution_path)

        fitness = self.fitness_evaluator.calcFitness(maze_obj,"IMPROVED")
        print("Fitness:",fitness)

        save_ask = input("Save Maze? (y/n): ")
        if save_ask == "y":
             maze_id = input("Maze Name?:")

             self.maze_data_storage.save_maze_data(maze_obj,maze_id)

    def createGAMaze(self,size,generating_mode,pop_size,fitness_function,hyperparameters,generations):
        maze_obj=self.maze_generator.geneticAlgorithmMaze(size,generating_mode,pop_size,fitness_function,hyperparameters,generations)

        self.maze_renderer.renderPathInMaze(maze_obj,maze_obj.solution_path)


    #Ertellt eine Beispiel Population und wertet die Daten aus
    def createPopulation(self,size_maze=25,generating_mode="RANDOM",size_pop=100,fitness_function="IMPROVED",generations=300):
        #Analyse-Beobachter erstellen
        testAnalyzer = population_analyzer.PopulationAnalyzer()

        #Einen Populationsverwalter erstellen
        popM = population_manager.PopulationManager(size_maze, generating_mode,size_pop, fitness_function)

        #Analyse-Beobachter als Beobachter für Populationsverwalter hinzufügen
        popM.addObserver(testAnalyzer)
        #Population evolvieren
        popM.runPopulation(generations)

        #Analyseergebnisse darstellen
        testAnalyzer.render_fittest()
        testAnalyzer.plot_fitness_convergence()
        testAnalyzer.plot_diversity()


    def createComparer(self):
        ac = algorithm_comparer.AlgorithmComparer(30,100,[self.maze_generator.MODE_RANDOM,self.maze_generator.MODE_RANDOM_DFS])
        ac.plot_compare_results(ac.compareSet())
