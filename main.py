import fitness_evaluator
import maze_generator as mg
import path_finder as pf
import maze_renderer as mr
import genetic_operator


def testMethod():

    testGen = mg.MazeGenerator()
    testRenderer = mr.MazeRenderer()
    pathFinder = pf.PathFinder()
    testGO = genetic_operator.GeneticOperator()

    for i in range(100):

        testMaze = testGen.generateMaze(25, "RANDOM")
        path = pathFinder.generatePath(testMaze)

        print(f"Labyrinth {i+1}/100 - Pfadlänge: {testMaze.shortestPath}")

        testRenderer.renderPathInMaze(testMaze, path)
#Programmeinstiegspunkt
if __name__ == '__main__':

    testMethod()

    while True:
        pass



