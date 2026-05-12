import fitness_evaluator
import maze_generator as mg
import path_finder as pf
import maze_renderer as mr
import genetic_operator


def testMethod():

    #Ein Labyrinth generieren
    testGen = mg.MazeGenerator()
    testMaze = testGen.generateMaze(25, "RANDOM_DFS")


    testRenderer = mr.MazeRenderer()


    #Eine Pfadsuche auf Labyrinth ausfürhen
    pathFinder = pf.PathFinder()
    path = pathFinder.generatePath(testMaze, "BFS")


    #Einen Pfad in Labyrinth visualisieren
    testRenderer.renderPathInMaze(testMaze, path)

    print("")
    print("Pfadlänge: "+str(testMaze.shortestPath))
    print("Sackgassen: "+str(testMaze.deadEndCount))
    print("Dichte: "+str(testMaze.density))

    print("")

    testFE = fitness_evaluator.FitnessEvaluator()
    fitness = testFE.calcFitness(testMaze)
    print("Fitness: "+str(fitness))

    testGO = genetic_operator.GeneticOperator()
    testGO.mutate(testMaze)

    print("")
    path = pathFinder.generatePath(testMaze, "BFS")
    testRenderer.renderPathInMaze(testMaze, path)

    print("")
    print("Pfadlänge: " + str(testMaze.shortestPath))
    print("Sackgassen: " + str(testMaze.deadEndCount))
    print("Dichte: " + str(testMaze.density))

    print("")
    fitness = testFE.calcFitness(testMaze)
    print("Fitness: " + str(fitness))


#Programmeinstiegspunkt
if __name__ == '__main__':

    testMethod()

    while True:
        pass



