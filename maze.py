class Maze:



    VALUE_EMPTY = "EMPTY"
    VALUE_WALL = "WALL"
    VALUE_START = "START"
    VALUE_END = "END"


    matrix=[]

    def __init__(self,matrix,startPos=(-1,-1),endPos=(-1,-1)):
        self.matrix = matrix
        self.start = startPos
        self.end = endPos



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


    #Berechnet die Anzahl an Sackgassen im Labyrinth
    def countDeadEnds(self):

        deadEnds = 0

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):

                if self.matrix[i][j] == Maze.VALUE_EMPTY or self.matrix[i][j] == Maze.VALUE_START or self.matrix[i][j] == Maze.VALUE_END:
                    if len(self.checkForNeighbors((i,j),1,self.VALUE_WALL))==1:
                        deadEnds += 1

        return deadEnds
