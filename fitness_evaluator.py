import math
import metric_analyzer

class FitnessEvaluator:

    FUNCTION_BASE = "BASE"
    FUNCTION_IMPROVED = "IMPROVED"

    DEFAULT_FUNCTION = FUNCTION_IMPROVED


    SHORTEST_PATH_WEIGHT = 1
    DEAD_END_WEIGHT= 0.5
    DENSITY_WEIGHT = -0.3

    CONNECTIVITY_WEIGHT = 1.5

    def calcFitness(self,maze,function=DEFAULT_FUNCTION):

        if function==self.FUNCTION_BASE:
            return self.BaseFitnessFunction(maze)
        elif function==self.FUNCTION_IMPROVED:
            return self.ImprovedFitnessFuction(maze)

    #Standard Fitnessfunktion aus Aufgabenstellung
    def BaseFitnessFunction(self,maze,metricAnalyzer=metric_analyzer.MetricAnalyzer()):
        shortestPath = metricAnalyzer.calcShortestPathMetric(maze)
        deadEndCount = metricAnalyzer.countDeadEnds(maze)
        density = metricAnalyzer.calcDensityMetric(maze)

        return shortestPath * self.SHORTEST_PATH_WEIGHT + deadEndCount * self.DEAD_END_WEIGHT + density * self.DENSITY_WEIGHT

    #Erweiterte bzw. abgeänderte Fitnessfunktion
    def ImprovedFitnessFuction(self,maze,metricAnalyzer=metric_analyzer.MetricAnalyzer()):
        shortestPath = metricAnalyzer.calcShortestPathMetric(maze)
        density = metricAnalyzer.calcDensityMetric(maze)
        connectivity = metricAnalyzer.calcConnectivityMetric(maze)

        return shortestPath*self.SHORTEST_PATH_WEIGHT +(math.fabs(1-density))*self.DENSITY_WEIGHT+ connectivity * self.CONNECTIVITY_WEIGHT