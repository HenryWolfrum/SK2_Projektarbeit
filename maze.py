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
