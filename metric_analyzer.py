import math
from collections import deque

class MetricAnalyzer:


    #Berechnet das Verhältnis kürzester Pfad zu Manhattan Distanz
    def calcShortestPathMetric(self, maze):
        shortest_path_length = len(maze.solution_path)

        return shortest_path_length/(len(maze.matrix)**2)

    #Berechnet die Abweichung des Wand/Freifläche Verhältnis von 1
    def calcDensityMetric(self,maze):

        # Gemeinsame Hilfsfunktion vermeidet doppelten Loop mit calcConnectivityMetric
        wallCount = self._countWalls(maze)


        return 1-math.fabs(1-(wallCount /(len(maze.matrix)**2) ))

    # Belohnt zusammenhängende Wände (0 = alle isoliert, 1 = alle verbunden)
    def calcWallCohesionMetric(self, maze):
        matrix = maze.matrix
        wallCells = 0
        connectedWallCells = 0

        for i in range(len(matrix)):
            for j in range(len(matrix)):

                if matrix[i][j] != maze.VALUE_WALL:
                    continue

                wallCells += 1

                # Wand gilt als verbunden wenn min. ein Wand-Nachbar existiert
                wallNeighbors = maze.checkForNeighbors((i, j), 1, maze.VALUE_EMPTY)
                if len(wallNeighbors) < 4:
                    connectedWallCells += 1

        if wallCells == 0:
            return 0

        return connectedWallCells / wallCells

    # Berechnet den Anteil der Sackgassen an allen freien Zellen (0 = keine, 1 = alle)
    def calcDeadEndMetric(self, maze):
        matrix = maze.matrix
        deadEnds = 0
        freeCells = 0

        for i in range(len(matrix)):
            for j in range(len(matrix)):

                if matrix[i][j] == maze.VALUE_WALL:
                    continue

                freeCells += 1

                # Sackgasse = freie Zelle mit genau einem freien Nachbarn
                if len(maze.checkForNeighbors((i, j), 1, maze.VALUE_WALL)) == 1:
                    deadEnds += 1

        if freeCells == 0:
            return 0

        return deadEnds / freeCells


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
        totalCells = len(matrix) ** 2

        # Gemeinsame Hilfsfunktion vermeidet doppelten Loop mit calcDensityMetric
        wallCells = self._countWalls(maze)

        visited = set()
        frontier = deque([start])

        while frontier:

            current = frontier.popleft()  # Fix: war deque.popleft(frontier)

            if current in visited:
                continue

            reachableCells += 1

            visited.add(current)
            neighbors = maze.checkForNeighbors(current, 1, maze.VALUE_WALL)

            for neighbor in neighbors:
                if neighbor not in visited:
                    frontier.append(neighbor)

        return reachableCells,totalCells,wallCells

    # Hilfsfunktion: vermeidet doppelten Wall-Loop in calcDensityMetric und compareReachableSpace
    def _countWalls(self,maze):
        wallCount = 0

        matrix = maze.matrix

        for i in range(len(matrix)):
            for j in range(len(matrix)):

                if matrix[i][j] == maze.VALUE_WALL:
                    wallCount += 1

        return wallCount

