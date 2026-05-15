import path_finder
import math
from collections import deque

class MetricAnalyzer:

    #Berechnet das Verhältnis kürzester Pfad zu Manhattan Distanz
    def calcShortestPathMetric(self,maze):

        #Berechnet den aktuell kürzesten Pfad
        shortest_path_length = len(path_finder.PathFinder().generatePath(maze))

        #Manhattan Distanz
        manhattan_distance = math.fabs(maze.start[0]-maze.end[0])+math.fabs(maze.start[1]-maze.end[1])

        #Gib Verhältnis zurück um Wert relativ auszudrücken
        return shortest_path_length/manhattan_distance


    #Berechnet absolute Anzahl an Sackgassen
    def countDeadEnds(self,maze):
            deadEnds = 0

            matrix=maze.matrix

            for i in range(len(matrix)):
                for j in range(len(matrix)):

                    if matrix[i][j] != maze.VALUE_EMPTY:
                        if len(maze.checkForNeighbors((i, j), 1, maze.VALUE_WALL)) == 1:
                            deadEnds += 1

            return deadEnds

    #Berechnet die Abweichung des Wand/Freifläche Verhältnis von 1
    def calcDensityMetric(self,maze):
        wallCount = 0

        matrix=maze.matrix

        for i in range(len(matrix)):
            for j in range(len(matrix)):

                if matrix[i][j] == maze.VALUE_WALL:
                    wallCount += 1

        nonWallCount = (len(matrix)**2) - wallCount

        return math.fabs(1-(wallCount / nonWallCount))

    #Berechnet das Verhältnis Erreichbare Freifläche / Freifläche
    def calcConnectivityMetric(self,maze):
        result = self.compareReachableSpace(maze)

        reachableCells = result[0]
        totalCells = result[1]
        wallCells = result[2]

        if totalCells==wallCells:
            print("SCHWERER FEHLER: Maze besteht nur aus Wänden!")
            return -1

        connectivity = reachableCells/(totalCells-wallCells)

        return connectivity


    #Hilfsfunktion für Connectivity Metrik Berechnung
    def compareReachableSpace(self,maze):
        matrix = maze.matrix
        start = maze.start

        reachableCells = 0
        wallCells = 0
        totalCells = len(matrix) ** 2

        visited = set()
        frontier = deque([start])

        while frontier:

            current = deque.popleft(frontier)

            if current in visited:
                continue

            reachableCells += 1

            visited.add(current)
            neighbors = maze.checkForNeighbors(current, 1, maze.VALUE_WALL)

            for neighbor in neighbors:
                if neighbor not in visited:
                    frontier.append(neighbor)

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == maze.VALUE_WALL:
                    wallCells += 1

        return reachableCells,totalCells,wallCells