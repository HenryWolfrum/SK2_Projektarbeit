import maze


class MazeRenderer:

    RENDER_EMPTY ="\033[42m  \033[0m"
    RENDER_WALL = "\033[41m  \033[0m"
    RENDER_START = "\033[43m  \033[0m"
    RENDER_END = "\033[44m  \033[0m"

    RENDER_PATH= "\033[45m  \033[0m"

    RENDER_ERROR = "\033[35m??\033[0m"

    def __init__(self):
        pass

    def renderMaze(self,maze):
        matrix=maze.matrix

        for j in range(len(matrix)-1,-1,-1):
            print("")
            for i in range(len(matrix)):
                print(self.getColorForValue(matrix[i][j]),end="")


    def renderPathInMaze(self,maze,path):
        matrix = maze.matrix

        for j in range(len(matrix) - 1, -1, -1):
            print("")
            for i in range(len(matrix)):

                if (i, j) in path and maze.start != (i, j) and maze.end != (i, j):
                    print(self.RENDER_PATH,end="")
                else:
                    print(self.getColorForValue(matrix[i][j]), end="")



    def getColorForValue(self,value):

        if value == maze.Maze.VALUE_START:
            return self.RENDER_START
        elif value == maze.Maze.VALUE_END:
            return self.RENDER_END
        elif value == maze.Maze.VALUE_EMPTY:
            return self.RENDER_EMPTY
        elif value == maze.Maze.VALUE_WALL:
            return self.RENDER_WALL
        else:
            return self.RENDER_ERROR