import maze_generator
import tester
import maze_renderer

#Programmeinstiegspunkt
if __name__ == '__main__':
    print("Halloo")
    hyperparams={"mutation_rate":0.2,
                 "survivor_rate":0.5,
                 "tournament_size":2}
    maze = maze_generator.MazeGenerator().geneticAlgorithmMaze(25,"RANDOM",100,"IMPROVED",hyperparams,400)

    maze_renderer.MazeRenderer().renderPathInMaze(maze,maze.solution_path)

    while True:
        pass



