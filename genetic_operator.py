import random
import maze
import path_finder
import copy

class GeneticOperator:




    def __init__(self):
        pass


    def mutate(self,maze,count):

       for i in range(count):

           randomRow = random.randint(0, len(maze.matrix) - 1)
           randomColumn = random.randint(0, len(maze.matrix) - 1)

           randomCell = maze.matrix[randomRow][randomColumn]

           if randomCell == maze.VALUE_EMPTY:

               maze.matrix[randomRow][randomColumn] = maze.VALUE_WALL

               pathFinder = path_finder.PathFinder()

               # Ein gültiger Pfad muss weiterhin existieren
               if len(pathFinder.generatePath(maze)) == 0:
                   maze.matrix[randomRow][randomColumn] = maze.VALUE_EMPTY

           elif randomCell == maze.VALUE_WALL:
               maze.matrix[randomRow][randomColumn] = maze.VALUE_EMPTY


       #NeuBerechnungen der Labyrinth Metriken
       maze.updateMetrics()



    def crossover(self,maze1,maze2):

        childMatrix1= copy.deepcopy(maze1.matrix)
        childMatrix2= copy.deepcopy(maze2.matrix)


        for i in range(0,len(maze1.matrix)):

                if random.random()<0.5:

                    for j in range(0, len(maze1.matrix[i])):

                        currentValue1 = maze1.matrix[i][j]
                        currentValue2 = maze2.matrix[i][j]

                        if currentValue1!=maze.Maze.VALUE_START and currentValue1!=maze.Maze.VALUE_END and currentValue2!=maze.Maze.VALUE_START and currentValue2!=maze.Maze.VALUE_END:

                            childMatrix1[i][j] = currentValue2
                            childMatrix2[i][j] = currentValue1

                    helperObject1=maze.Maze(childMatrix1,maze1.start,maze1.end)
                    helperObject2=maze.Maze(childMatrix2,maze2.start,maze2.end)


                    if helperObject1.shortestPath==0:

                        for j in range(0, len(maze1.matrix)):
                            childMatrix1[i][j] = maze1.matrix[i][j]

                    if helperObject2.shortestPath==0:
                        for j in range(0, len(maze2.matrix)):
                            childMatrix2[i][j] = maze2.matrix[i][j]

        return maze.Maze(childMatrix1,maze1.start,maze1.end),maze.Maze(childMatrix2,maze2.start,maze2.end)

