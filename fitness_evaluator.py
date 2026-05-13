class FitnessEvaluator:

    SHORTEST_PATH_WEIGHT = 10
    DEAD_END_WEIGHT= 2.5
    DENSITY_WEIGHT = 0.5

    def __init__(self):
        pass

    def calcFitness(self,maze):

        shortestPath = maze.shortestPath
        deadEndCount = maze.deadEndCount
        density = maze.density

        return shortestPath*self.SHORTEST_PATH_WEIGHT+deadEndCount*self.DEAD_END_WEIGHT+density*self.DENSITY_WEIGHT