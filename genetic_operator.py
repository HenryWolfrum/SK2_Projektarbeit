import random
from copy import deepcopy
import maze
import path_finder


class GeneticOperator:

    def mutate(self, m, count):
        for _ in range(count):
            row = random.randint(0, len(m.matrix) - 1)
            col = random.randint(0, len(m.matrix[0]) - 1)
            value = m.matrix[row][col]

            if value == maze.Maze.VALUE_EMPTY:
                m.change_matrix(row, col, maze.Maze.VALUE_WALL)
                if len(m.solution_path) == 0:
                    m.matrix[row][col] = value  # Matrix direkt setzen...
                    m.solution_path = path_finder.PathFinder().generatePath(m)  # ...und Pfad erzwingen
            else:
                m.change_matrix(row, col, maze.Maze.VALUE_EMPTY)

    def crossover(self, m1, m2):
        child1 = maze.Maze(deepcopy(m1.matrix), m1.start, m1.end)
        child2 = maze.Maze(deepcopy(m2.matrix), m2.start, m2.end)

        for i in range(len(m1.matrix)):
            if random.random() < 0.5:
                for j in range(len(m1.matrix[i])):
                    v1 = m1.matrix[i][j]
                    v2 = m2.matrix[i][j]
                    if v1 == v2:
                        continue

                    child1.change_matrix(i, j, v2)
                    if len(child1.solution_path) == 0:
                        child1.matrix[i][j] = v1
                        child1.solution_path = path_finder.PathFinder().generatePath(child1)

                    child2.change_matrix(i, j, v1)
                    if len(child2.solution_path) == 0:
                        child2.matrix[i][j] = v2
                        child2.solution_path = path_finder.PathFinder().generatePath(child2)

        return child1, child2