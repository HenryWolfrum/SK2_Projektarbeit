import fitness_evaluator
import maze
import maze_generator
import maze_generator as mg
import maze_renderer
import path_finder
import population_manager
import population_analyzer

class Tester:

    def createMaze(self,size=25,mode="RANDOM"):
        #Labyrinth generieren
        maze=maze_generator.MazeGenerator().generateMaze(size,mode)

        #Lösungspfad generieren
        path=path_finder.PathFinder().generatePath(maze)

        #Labyrinth visualisieren mit Pfad
        maze_renderer.MazeRenderer().renderPathInMaze(maze,path)

    def createPopulation(self,size_maze=25,generating_mode="RANDOM",size_pop=100,fitness_function="IMPROVED",generations=200):
        #Analyse Beobachter erstellen
        testAnalyzer = population_analyzer.PopulationAnalyzer()

        #Einen Populationsverwalter erstellen
        popM = population_manager.PopulationManager(size_maze, generating_mode,size_pop, fitness_function)

        #Analyse Beobachter als Beobachter für Populationsverwalter hinzufügen
        popM.addObserver(testAnalyzer)
        #Population evolvieren
        popM.runPopulation(generations)

        #Analyseergebnisse darstellen
        testAnalyzer.plot_fitness_convergence()
        testAnalyzer.plot_diversity()
