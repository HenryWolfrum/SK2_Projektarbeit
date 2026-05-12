import random
import maze
import path_finder

class GeneticOperator:

    def __init__(self):
        pass


    def mutate(self,maze):

        randomRow = random.randint(0,len(maze.matrix)-1)
        randomColumn = random.randint(0,len(maze.matrix)-1)

        randomCell = maze.matrix[randomRow][randomColumn]

        if randomCell == maze.VALUE_EMPTY:

            maze.matrix[randomRow][randomColumn] = maze.VALUE_WALL

            pathFinder = path_finder.PathFinder()

            #Ein gültiger Pfad muss weiterhin existieren
            if len(pathFinder.generatePath(maze))==0:
                maze.matrix[randomRow][randomColumn] = maze.VALUE_EMPTY

        elif randomCell == maze.VALUE_WALL:
            maze.matrix[randomRow][randomColumn] = maze.VALUE_EMPTY


        #NeuBerechnungen der Labyrinth Metriken
        maze.updateMetrics()