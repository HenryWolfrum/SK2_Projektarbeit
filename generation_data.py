import maze_renderer
import path_finder

class GenerationData:

    def __init__(self,generation,max_fitness,average_fitness,min_fitness,fittest_maze,weakest_maze):
        self.generation = generation
        self.max_fitness = max_fitness
        self.average_fitness = average_fitness
        self.min_fitness = min_fitness
        self.fittest_maze=fittest_maze
        self.weakest_maze=weakest_maze


    def printData(self):
        print("Generation:",self.generation)
        print("Max fitness:",self.max_fitness)
        print("Average fitness:",self.average_fitness)
        print("Min fitness:",self.min_fitness)

        renderer = maze_renderer.MazeRenderer()
        pathfinder = path_finder.PathFinder()
        print("Strongest Maze:")
        strongest_path = pathfinder.generatePath(self.fittest_maze)
        renderer.renderPathInMaze(self.fittest_maze,strongest_path)
        print("")
        print("Weakest Maze:")
        weakest_path = pathfinder.generatePath(self.weakest_maze)
        renderer.renderPathInMaze(self.weakest_maze,weakest_path)

