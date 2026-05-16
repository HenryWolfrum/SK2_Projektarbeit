import math
import metric_analyzer

class FitnessEvaluator:

    FUNCTION_BASE = "BASE"
    FUNCTION_IMPROVED = "IMPROVED"

    DEFAULT_FUNCTION = FUNCTION_IMPROVED


    SHORTEST_PATH_WEIGHT = 0.5
    DEAD_END_WEIGHT= 0.2
    DENSITY_WEIGHT = -0.1

    CONNECTIVITY_WEIGHT = 0.3

    WALL_COHESION_WEIGHT = 0.3

    def calcFitness(self,maze,function=DEFAULT_FUNCTION):

        if function==self.FUNCTION_BASE:
            return self.BaseFitnessFunction(maze)
        elif function==self.FUNCTION_IMPROVED:
            return self.ImprovedFitnessFuction(maze)

    #Standard Fitnessfunktion aus Aufgabenstellung
    def BaseFitnessFunction(self,maze,metricAnalyzer=metric_analyzer.MetricAnalyzer()):
        shortestPath = metricAnalyzer.calcShortestPathMetric(maze)
        deadEndCount = metricAnalyzer.calcDeadEndMetric(maze)
        density = metricAnalyzer.calcDensityMetric(maze)

        return shortestPath * self.SHORTEST_PATH_WEIGHT + deadEndCount * self.DEAD_END_WEIGHT + density * self.DENSITY_WEIGHT

    #Erweiterte bzw. abgeänderte Fitnessfunktion
    def ImprovedFitnessFuction(self,maze,metricAnalyzer=metric_analyzer.MetricAnalyzer()):
        shortestPath = metricAnalyzer.calcShortestPathMetric(maze)
        densityMetric = metricAnalyzer.calcDensityMetric(maze)
        connectivity = metricAnalyzer.calcConnectivityMetric(maze)
        deadEndCount = metricAnalyzer.calcDeadEndMetric(maze)
        wallcohesion = metricAnalyzer.calcWallCohesionMetric(maze)

        return shortestPath*self.SHORTEST_PATH_WEIGHT +densityMetric*self.DENSITY_WEIGHT+ connectivity * self.CONNECTIVITY_WEIGHT+deadEndCount * self.DEAD_END_WEIGHT+wallcohesion * self.WALL_COHESION_WEIGHT