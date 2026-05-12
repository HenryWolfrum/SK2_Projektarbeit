import maze
import random
import path_finder

class MazeGenerator:

    DEFAULT_SIZE = 25
    DEFAULT_MODE = "RANDOM_DFS"


    def __init__(self,mode="DEFAULT"):
        self.mode = mode




    def generateMaze(self,size=DEFAULT_SIZE,mode=DEFAULT_MODE):

        if(mode=="RANDOM_DFS"):
            result = self.randomizedDFSMaze(size)

            return result

        elif(mode=="RANDOM"):
            result = self.randomizedMaze(size)

            return result




#Implementierung von RandomizedDFS für Labyrinthgenerierung

    def randomizedDFSMaze(self,size=DEFAULT_SIZE):

        #Start Matrix
        matrix = [[maze.Maze.VALUE_WALL for _ in range(size)] for _ in range(size)]

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
                matrix[end[0]][end[1]] = maze.Maze.VALUE_END

            visited.add(current)

            matrix[current[0]][current[1]] = maze.Maze.VALUE_EMPTY

            neighbors = maze.Maze.checkForNeighbors(maze.Maze(matrix),current,2,maze.Maze.VALUE_EMPTY)

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

        #Start und Ziel als Werte setzen
        matrix[start[0]][start[1]] = maze.Maze.VALUE_START
        matrix[end[0]][end[1]] = maze.Maze.VALUE_END

        return maze.Maze(matrix, start, end)


#Generierte einen zufälligen Pfad von Start->Ziel. Der Rest des Labyrinths ist randomisiert
    def randomizedMaze(self,size=DEFAULT_SIZE):

        # Start Matrix
        matrix = [[maze.Maze.VALUE_WALL for _ in range(size)] for _ in range(size)]

        #Zufälligen Start und Ziel wählen
        start = (random.randint(0,size-1), random.randint(0,size-1))
        end = (random.randint(0,size-1), random.randint(0,size-1))

        while end==start:
            end = (random.randint(0,size-1), random.randint(0,size-1))


        #Zufällige Pfad Generierung

        visited = set()
        frontier = [start]
        current = (-1,-1)

        while current != end:

            current = frontier.pop()



            visited.add(current)

            matrix[current[0]][current[1]] = maze.Maze.VALUE_EMPTY

            neighbors=[]

            #Nachbarn prüfen (simpel)
            if current[0]!=size-1:
                neighbors.append((current[0]+1, current[1]))
            if current[0]!=0:
                neighbors.append((current[0]-1, current[1]))
            if current[1]!=size-1:
                neighbors.append((current[0], current[1]+1))
            if current[1]!=0:
                neighbors.append((current[0], current[1]-1))

            random.shuffle(neighbors)

            for neighbor in neighbors:
                if neighbor not in visited:
                    frontier.append(neighbor)

        #Start und Ziel setzen
        matrix[start[0]][start[1]] = maze.Maze.VALUE_START
        matrix[end[0]][end[1]] = maze.Maze.VALUE_END

        #Pfad herausfinden
        helperObject = maze.Maze(matrix, start, end)
        path = path_finder.PathFinder().generatePath(helperObject)

        #Restliches Labyrinth randomisieren
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if (i,j) not in path:
                    if random.random()<0.5:
                        matrix[i][j] = maze.Maze.VALUE_EMPTY
                    else:
                        matrix[i][j] = maze.Maze.VALUE_WALL


        return maze.Maze(matrix, start, end)