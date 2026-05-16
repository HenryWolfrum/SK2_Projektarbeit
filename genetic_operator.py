import random
import maze
import path_finder
import copy
import metric_analyzer

class GeneticOperator:

    def mutate(self, maze, count):
        # PathFinder einmal instanziieren, nicht pro Iteration
        pathFinder = path_finder.PathFinder()

        for i in range(count):
            randomRow = random.randint(0, len(maze.matrix) - 1)
            randomColumn = random.randint(0, len(maze.matrix) - 1)
            randomCell = maze.matrix[randomRow][randomColumn]

            if randomCell == maze.VALUE_EMPTY:
                maze.matrix[randomRow][randomColumn] = maze.VALUE_WALL

                # Nur prüfen wenn Wand gesetzt wird (Entfernen kann Pfad nie blockieren)
                if len(pathFinder.generatePath(maze)) == 0:
                    maze.matrix[randomRow][randomColumn] = maze.VALUE_EMPTY

            elif randomCell == maze.VALUE_WALL:
                # Kein Check nötig: Wand entfernen blockiert nie den Pfad
                maze.matrix[randomRow][randomColumn] = maze.VALUE_EMPTY

    def crossover(self, maze1, maze2):
        childMatrix1 = copy.deepcopy(maze1.matrix)
        childMatrix2 = copy.deepcopy(maze2.matrix)

        analyzer = metric_analyzer.MetricAnalyzer()  # Einmal instanziieren

        # Alle Zeilen-Swaps sammeln, DANN einmal validieren
        swapped_rows = []

        for i in range(len(maze1.matrix)):
            if random.random() < 0.5:
                for j in range(len(maze1.matrix[i])):
                    v1 = maze1.matrix[i][j]
                    v2 = maze2.matrix[i][j]

                    if (v1 != maze.Maze.VALUE_START and v1 != maze.Maze.VALUE_END and
                            v2 != maze.Maze.VALUE_START and v2 != maze.Maze.VALUE_END):
                        childMatrix1[i][j] = v2
                        childMatrix2[i][j] = v1

                swapped_rows.append(i)

        # Einmaliger Validierungs-Check am Ende statt nach jeder Zeile
        if swapped_rows:
            helper1 = maze.Maze(childMatrix1, maze1.start, maze1.end)
            helper2 = maze.Maze(childMatrix2, maze2.start, maze2.end)

            if analyzer.calcShortestPathMetric(helper1) == 0:
                # Nur getauschte Zeilen zurücksetzen, nicht die gesamte Matrix
                for i in swapped_rows:
                    for j in range(len(maze1.matrix[i])):
                        childMatrix1[i][j] = maze1.matrix[i][j]

            if analyzer.calcShortestPathMetric(helper2) == 0:
                for i in swapped_rows:
                    for j in range(len(maze2.matrix[i])):
                        childMatrix2[i][j] = maze2.matrix[i][j]

        return maze.Maze(childMatrix1, maze1.start, maze1.end), \
               maze.Maze(childMatrix2, maze2.start, maze2.end)