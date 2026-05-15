import math
import metric_analyzer

class FitnessEvaluator:

    DEFAULT_FUNCTION = "BASE"


    SHORTEST_PATH_WEIGHT = 1
    DEAD_END_WEIGHT= 0.5
    DENSITY_WEIGHT = -0.3

    CONNECTIVITY_WEIGHT = 1.5

    def calcFitness(self,maze,function=DEFAULT_FUNCTION):

        if function=="BASE":
            return self.BaseFitnessFunction(maze)
        elif function=="IMPROVED":
            return self.ImprovedFitnessFuction(maze)


    def BaseFitnessFunction(self,maze,metricAnalyzer=metric_analyzer.MetricAnalyzer()):
        shortestPath = metricAnalyzer.calcShortestPathMetric(maze)
        deadEndCount = metricAnalyzer.countDeadEnds(maze)
        density = metricAnalyzer.calcDensity(maze)

        return shortestPath * self.SHORTEST_PATH_WEIGHT + deadEndCount * self.DEAD_END_WEIGHT + density * self.DENSITY_WEIGHT


    def ImprovedFitnessFuction(self,maze,metricAnalyzer=metric_analyzer.MetricAnalyzer()):
        shortestPath = metricAnalyzer.calcShortestPathMetric(maze)
        density = metricAnalyzer.calcDensity(maze)
        connectivity = metricAnalyzer.calcConnectivity(maze)

        return shortestPath*self.SHORTEST_PATH_WEIGHT +(math.fabs(1-density))*self.DENSITY_WEIGHT+ connectivity * self.CONNECTIVITY_WEIGHT