import maze_generator as mg
import path_finder as pf
import maze_renderer as mr



def testMethod():

    #Ein Labyrinth generieren
    testGen = mg.MazeGenerator()
    testMaze = testGen.generateMaze(2, "RANDOM_DFS")

    #Ein Labyrinth visualisieren
    testRenderer = mr.MazeRenderer()
    testRenderer.renderMaze(testMaze)

    #Eine Pfadsuche auf Labyrinth ausfürhen
    pathFinder = pf.PathFinder()
    path = pathFinder.generatePath(testMaze, "BFS")

    print("")
    print("")

    #Einen Pfad in Labyrinth visualisieren
    testRenderer.renderPathInMaze(testMaze, path)

    print("")
    print(testMaze.countDeadEnds())

    print(testMaze.calcDensity())

#Programmeinstiegspunkt
if __name__ == '__main__':

    testMethod()

    while True:
        pass



