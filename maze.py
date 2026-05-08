class Maze:

    matrix=[]

    def __init__(self,matrix,startPos=(-1,-1),endPos=(-1,-1)):
        self.matrix = matrix
        self.startPos = startPos
        self.endPos = endPos

    def toString(self):
        for i in range(len(self.matrix)):
            print("")
            for j in range(len(self.matrix[i])):
                print(" "+str(self.matrix[i][j]),end="")