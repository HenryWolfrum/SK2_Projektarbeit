import fitness_evaluator
import maze_generator as mg
import path_finder as pf
import maze_renderer as mr
import genetic_operator


def testMethod():

    #Ein Labyrinth generieren
    testGen = mg.MazeGenerator()

    testRenderer = mr.MazeRenderer()

    testGO = genetic_operator.GeneticOperator()

    #Eine Pfadsuche auf Labyrinth ausfürhen
    pathFinder = pf.PathFinder()

    testMaze2 = mg.MazeGenerator().generateMaze(25, "RANDOM_DFS")
    testMaze3 = mg.MazeGenerator().generateMaze(25, "RANDOM_DFS")

    path1=pathFinder.generatePath(testMaze2, "BFS")
    testRenderer.renderPathInMaze(testMaze2,path1)

    print("")
    path2=pathFinder.generatePath(testMaze3, "BFS")
    testRenderer.renderPathInMaze(testMaze3,path2)
    print("")

    cross = testGO.crossover(testMaze2,testMaze3)

    child1=cross[0]
    child2=cross[1]

    path3=pathFinder.generatePath(child1, "BFS")
    path4=pathFinder.generatePath(child2, "BFS")

    print("")
    print("")
    testRenderer.renderPathInMaze(child1,path3)
    print("")
    testRenderer.renderPathInMaze(child2,path4)

#Programmeinstiegspunkt
if __name__ == '__main__':

    testMethod()

    while True:
        pass



