import maze_generator as mg
import path_finder as pf

if __name__ == '__main__':
    testGen = mg.MazeGenerator()
    testMaze = testGen.generateMaze(50,"RANDOM_DFS")
    testMaze.toString()



    pathFinder = pf.PathFinder()
    path =pathFinder.generatePath(testMaze,"BFS")

    print("")
    print("")
    pathFinder.printPath(testMaze,path)


    while True:
        pass



