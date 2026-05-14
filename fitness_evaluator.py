import math

class FitnessEvaluator:

    DEFAULT_FUNCTION = "BASE"


    SHORTEST_PATH_WEIGHT = 1
    DEAD_END_WEIGHT= 0.5
    DENSITY_WEIGHT = -0.8

    UNREACHABLE_CELL_WEIGHT = -1

    def __init__(self):
        pass

    def calcFitness(self,maze,function=DEFAULT_FUNCTION):
        if function=="BASE":
            return self.BaseFitnessFunction(maze)
        elif function=="IMPROVED":
            return self.ImprovedFitnessFuction(maze)


    def BaseFitnessFunction(self,maze):
        shortestPath = maze.shortestPath
        deadEndCount = maze.deadEndCount
        density = maze.density

        return shortestPath * self.SHORTEST_PATH_WEIGHT + deadEndCount * self.DEAD_END_WEIGHT + density * self.DENSITY_WEIGHT


    def ImprovedFitnessFuction(self,maze):
        shortestPath = maze.shortestPath
        deadEndCount = maze.deadEndCount
        density = maze.density
        unreachableCells = maze.unreachableCells

        return shortestPath*self.SHORTEST_PATH_WEIGHT + deadEndCount*self.DEAD_END_WEIGHT +(math.fabs(1-density))*self.DENSITY_WEIGHT+ unreachableCells * self.UNREACHABLE_CELL_WEIGHT