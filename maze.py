import path_finder
from collections import deque

class Maze:



    VALUE_EMPTY = "EMPTY"
    VALUE_WALL = "WALL"
    VALUE_START = "START"
    VALUE_END = "END"


    matrix=[]

    startPos=(-1,-1)
    endPos=(-1,-1)


    def __init__(self,matrix,startPos,endPos):
        self.matrix = matrix
        self.start = startPos
        self.end = endPos

        self.shortestPath = len(path_finder.PathFinder().generatePath(self))
        self.deadEndCount = self.countDeadEnds()
        self.density = self.calcDensity()
        self.unreachableCells = self.countUnreachableCells()

        self.fitness = -1



    #Sammelt alle horizontalen Nachbarn, welche dist Einheiten von pos entfernt sind und nicht compareValue entsprechen
    def checkForNeighbors(self, pos, dist, compareValue):

            matrix = self.matrix

            neighbors = []
            size = len(matrix)

            # oben
            if pos[0] > dist-1 and not matrix[pos[0] - dist][pos[1]] == compareValue:
                neighbors.append((pos[0] - dist, pos[1]))

            # unten
            if pos[0] < size - dist and not matrix[pos[0] + dist][pos[1]] == compareValue:
                neighbors.append((pos[0] +dist, pos[1]))

            # links
            if pos[1] > dist-1 and not matrix[pos[0]][pos[1] - dist] == compareValue:
                neighbors.append((pos[0], pos[1] - dist))

            # rechts
            if pos[1] < size - dist and not matrix[pos[0]][pos[1] + dist] == compareValue:
                neighbors.append((pos[0], pos[1] + dist))

            return neighbors


    def getShortestPathLength(self):
        return len(path_finder.PathFinder().generatePath(self))

    #Berechnet die Anzahl an Sackgassen im Labyrinth
    def countDeadEnds(self):
        deadEnds = 0

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):

                if self.matrix[i][j] == Maze.VALUE_EMPTY or self.matrix[i][j] == Maze.VALUE_START or self.matrix[i][j] == Maze.VALUE_END:
                    if len(self.checkForNeighbors((i,j),1,self.VALUE_WALL))==1:
                        deadEnds += 1

        return deadEnds

    def calcDensity(self):
        wallCount=0

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):

                if self.matrix[i][j] == Maze.VALUE_WALL:
                    wallCount+=1

        nonWallCount=(len(self.matrix)*len(self.matrix))-wallCount

        return wallCount/nonWallCount


    def countUnreachableCells(self):
        reachableCells = 0

        wallCells = 0
        totalCells = len(self.matrix)**2

        visited = set()
        frontier = deque([self.start])

        while frontier:

            current = deque.popleft(frontier)


            if current in visited:
                continue

            reachableCells += 1

            visited.add(current)
            neighbors = self.checkForNeighbors(current, 1, self.VALUE_WALL)

            for neighbor in neighbors:
                if neighbor not in visited:
                    frontier.append(neighbor)

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == Maze.VALUE_WALL:
                    wallCells+=1

        return totalCells - (reachableCells+wallCells)






    def updateMetrics(self):
        self.shortestPath = self.getShortestPathLength()
        self.deadEndCount = self.countDeadEnds()
        self.density = self.calcDensity()

    def setFitness(self,fitness_value):

        if fitness_value ==None:
            print("FEHLER: Wertzuweisung für Fitness ist NONE!")
        else:
            self.fitness = fitness_value

