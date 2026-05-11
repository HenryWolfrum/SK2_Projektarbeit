import maze_generator as mg
import path_finder as pf
import maze_renderer as mr

if __name__ == '__main__':
    testGen = mg.MazeGenerator()
    testMaze = testGen.generateMaze(25,"RANDOM_DFS")

    testRenderer = mr.MazeRenderer()
    testRenderer.renderMaze(testMaze)



    pathFinder = pf.PathFinder()
    path =pathFinder.generatePath(testMaze,"BFS")

    print("")
    print("")
    testRenderer.renderPathInMaze(testMaze,path)

    print("")
    print("Die kürzeste Pfadlänge beträgt: "+str(len(path)))


    while True:
        pass



