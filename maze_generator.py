import maze
import random

class MazeGenerator:

    DEFAULT_SIZE = 25



    def __init__(self,mode="DEFAULT"):
        self.mode = mode




    def generateMaze(self,size=DEFAULT_SIZE,mode="DEFAULT"):

        matrix = [[maze.Maze.VALUE_WALL for _ in range(size)] for _ in range(size)]

        if(mode=="RANDOM_DFS"):
            result = self.randomizedDFSMaze(matrix)
            matrix = result[0]

            #Start setzen
            start = result[1]
            matrix[start[0]][start[1]] = maze.Maze.VALUE_START

            #Ende setzen
            end = result[2]
            matrix[end[0]][end[1]] = maze.Maze.VALUE_END

            return maze.Maze(matrix, start, end)

        return maze.Maze(matrix,(0,0),(7,7))






#Implementierung von RandomizedDFS für Labyrinthgenerierung

    def randomizedDFSMaze(self,matrix):

        #Zufälligen Start wählen
        start = (random.randint(0, len(matrix) - 1), random.randint(0, len(matrix) - 1))

        visited = set()
        frontier = [start]

        counter=0
        end = (-1,-1)

        while frontier:

            counter+=1

            current = frontier.pop()

            if counter == (len(matrix)**2)//3:
                end=(current[0],current[1])



            visited.add(current)
            matrix[current[0]][current[1]] = maze.Maze.VALUE_EMPTY

            neighbors = self.checkForNeighbors(current, matrix)

            candidates = []

            for neighbor in neighbors:
                if neighbor not in visited:
                    candidates.append(neighbor)

            if candidates:
                next_cell = random.choice(candidates)

                # Wand entfernen
                wall_x = (current[0] + next_cell[0]) // 2
                wall_y = (current[1] + next_cell[1]) // 2

                matrix[wall_x][wall_y] = maze.Maze.VALUE_EMPTY

                frontier.append(current)
                frontier.append(next_cell)

        return (matrix,start,end)

    def checkForNeighbors(self, pos, matrix):

        neighbors = []
        size = len(matrix)

        # oben
        if pos[0] > 1 and matrix[pos[0] - 2][pos[1]] != maze.Maze.VALUE_EMPTY:
            neighbors.append((pos[0] - 2, pos[1]))

        # unten
        if pos[0] < size - 2 and matrix[pos[0] + 2][pos[1]] != maze.Maze.VALUE_EMPTY:
            neighbors.append((pos[0] + 2, pos[1]))

        # links
        if pos[1] > 1 and matrix[pos[0]][pos[1] - 2] != maze.Maze.VALUE_EMPTY:
            neighbors.append((pos[0], pos[1] - 2))

        # rechts
        if pos[1] < size - 2 and matrix[pos[0]][pos[1] + 2] != maze.Maze.VALUE_EMPTY:
            neighbors.append((pos[0], pos[1] + 2))

        return neighbors




