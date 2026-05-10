import maze_generator as mg

if __name__ == '__main__':
    testGen = mg.MazeGenerator()
    testMaze = testGen.generateMaze(50,"RANDOM_DFS")
    testMaze.toString()


