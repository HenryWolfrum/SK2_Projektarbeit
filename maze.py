import path_finder


class Maze:


    VALUE_EMPTY = "0"
    VALUE_WALL = "1"
    VALUE_START = "2"
    VALUE_END = "3"


    matrix=[]

    startPos=(-1,-1)
    endPos=(-1,-1)

    fitness=-1

    solution_path = []


    def __init__(self,matrix,startPos=(-1,-1),endPos=(-1,-1)):
        self.matrix = matrix
        self.start = startPos
        self.end = endPos

        self.solution_path = path_finder.PathFinder().generatePath(self)

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

    #Zum Ändern von Matrix Werten (inklusive Absicherungen)
    def change_matrix(self, row, col, value):
        if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[row]):

            if (row, col) == self.start or (row, col) == self.end or value==self.VALUE_START or value==self.VALUE_END:
                return  # Start/Ziel nie verändern
            self.matrix[row][col] = value

            if (row, col) in self.solution_path or len(self.solution_path) == 0:
                self.solution_path = path_finder.PathFinder().generatePath(self)

    def setFitness(self,fitness_value):

        if fitness_value ==None:
            print("FEHLER: Wertzuweisung für Fitness ist NONE!")
        else:
            self.fitness = fitness_value

