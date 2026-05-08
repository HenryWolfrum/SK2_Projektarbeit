import maze
import random

class MazeGenerator:

    DEFAULT_SIZE = 25

    VALUE_EMPTY = 0
    VALUE_WALL = 1
    VALUE_START = 2
    VALUE_END = 3

    def __init__(self,mode="DEFAULT"):
        self.mode = mode


    def generateMaze(self,size=DEFAULT_SIZE,mode="DEFAULT"):

        matrix = [[1 for _ in range(size)] for _ in range(size)]

        return maze.Maze(matrix,(0,0),(7,7))


