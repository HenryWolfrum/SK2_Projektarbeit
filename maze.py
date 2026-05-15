class Maze:


    VALUE_EMPTY = "EMPTY"
    VALUE_WALL = "WALL"
    VALUE_START = "START"
    VALUE_END = "END"


    matrix=[]

    startPos=(-1,-1)
    endPos=(-1,-1)

    fitness=-1

    def __init__(self,matrix,startPos,endPos):
        self.matrix = matrix
        self.start = startPos
        self.end = endPos


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



    def setFitness(self,fitness_value):

        if fitness_value ==None:
            print("FEHLER: Wertzuweisung für Fitness ist NONE!")
        else:
            self.fitness = fitness_value

