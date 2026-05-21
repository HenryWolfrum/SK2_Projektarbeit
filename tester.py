import fitness_evaluator
import maze
import maze_generator
import maze_generator as mg
import maze_renderer
import path_finder
import population_manager
import population_analyzer
import algorithm_comparer

class Tester:

    #Erstellt ein Beispiel Labyrinth und zeichnet es mit Lösungspfad
    def createMaze(self,size=25,mode="RANDOM"):
        #Labyrinth generieren
        maze=maze_generator.MazeGenerator().generateMaze(size,mode)

        #Lösungspfad generieren
        path=path_finder.PathFinder().generatePath(maze)

        #Labyrinth visualisieren mit Pfad
        maze_renderer.MazeRenderer().renderPathInMaze(maze,path)

        fitenss = fitness_evaluator.FitnessEvaluator().calcFitness(maze,"IMPROVED")
        print("fitenss:",fitenss)

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
        ac = algorithm_comparer.AlgorithmComparer(30,100,[maze_generator.MazeGenerator().MODE_RANDOM,maze_generator.MazeGenerator().MODE_RANDOM_DFS])
        ac.plot_compare_results(ac.compareSet())
