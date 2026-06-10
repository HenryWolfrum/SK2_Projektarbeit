import maze_renderer
import path_finder

class GenerationData:

    def __init__(self,generation,max_fitness,average_fitness,min_fitness,fittest_maze,weakest_maze,unique_ratio):
        self.generation = generation
        self.max_fitness = max_fitness
        self.average_fitness = average_fitness
        self.min_fitness = min_fitness
        self.fittest_maze=fittest_maze
        self.weakest_maze=weakest_maze
        self.unique_ratio = unique_ratio


    #Gibt das volle Datenpaket auf dem Bildschirm aus
    def printFullData(self):
        # ANSI Color Codes
        BOLD = "\033[1m"
        GREEN = "\033[92m"
        RED = "\033[91m"
        RESET = "\033[0m"

        print(f"\n📊 {BOLD}Generation {self.generation}{RESET}")
        print(f"📈 Max: {self.max_fitness}  |  Avg: {self.average_fitness}  |  Min: {self.min_fitness}")
        print("━" * 40)

        renderer = maze_renderer.MazeRenderer()
        pathfinder = path_finder.PathFinder()

        print(f"{GREEN}{BOLD}✦ Strongest Maze{RESET}")
        strongest_path = pathfinder.generatePath(self.fittest_maze)
        renderer.renderPathInMaze(self.fittest_maze, strongest_path)

        print(f"\n{RED}{BOLD}✦ Weakest Maze{RESET}")
        weakest_path = pathfinder.generatePath(self.weakest_maze)
        renderer.renderPathInMaze(self.weakest_maze, weakest_path)
        print("\n")

    #Gibt einen übersichtlichen Teil des Datenpakets auf dem Bildschirm aus
    def printReducedData(self):
        # ANSI Color Codes
        BOLD = "\033[1m"
        GREEN = "\033[92m"
        RED = "\033[91m"
        RESET = "\033[0m"

        print(f"\n📊 {BOLD}Generation {self.generation}{RESET}")
        print(f"📈 Max: {self.max_fitness}  |  Avg: {self.average_fitness}  |  Min: {self.min_fitness}")
        print("━" * 40)

