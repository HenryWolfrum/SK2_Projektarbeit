class Maze:


    VALUE_EMPTY = "0"
    VALUE_WALL = "1"
    VALUE_START = "2"
    VALUE_END = "3"


    matrix=[]

    startPos=(-1,-1)
    endPos=(-1,-1)

    fitness=-1

    def __init__(self,matrix,startPos=(-1,-1),endPos=(-1,-1)):
        self.matrix = matrix
        self.start = startPos
        self.end = endPos


        self.fitness = -1



    #Sammelt alle horizontalen/vertikalen Nachbarn, welche dist Einheiten von pos entfernt sind und nicht compareValue entsprechen
    def checkForNeighbors(self, pos, dist, compareValue):

            matrix = self.matrix

            neighbors = []
            size = len(matrix)

            # oben
            if pos[0] > dist-1 and matrix[pos[0] - dist][pos[1]] != compareValue:
                neighbors.append((pos[0] - dist, pos[1]))

            # unten
            if pos[0] < size - dist and matrix[pos[0] + dist][pos[1]] != compareValue:
                neighbors.append((pos[0] +dist, pos[1]))

            # links
            if pos[1] > dist-1 and matrix[pos[0]][pos[1] - dist] != compareValue:
                neighbors.append((pos[0], pos[1] - dist))

            # rechts
            if pos[1] < size - dist and matrix[pos[0]][pos[1] + dist] != compareValue:
                neighbors.append((pos[0], pos[1] + dist))

            return neighbors



    def setFitness(self,fitness_value):

        if fitness_value ==None:
            print("FEHLER: Wertzuweisung für Fitness ist NONE!")
        else:
            self.fitness = fitness_value

