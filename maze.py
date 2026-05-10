class Maze:

    matrix=[]

    def __init__(self,matrix,startPos=(-1,-1),endPos=(-1,-1)):
        self.matrix = matrix
        self.startPos = startPos
        self.endPos = endPos

    #Gibt die Matrix des Labyrinth aus, wobei die linke Ecke den Koordinatenursprung (0,0) definiert
    def toString(self):

        for j in range(len(self.matrix)-1,-1,-1):
            print("")
            for i in range(len(self.matrix)):
                print(str(self.matrix[i][j]),end="")

