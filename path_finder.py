from collections import deque
import maze

class PathFinder:

    DEFAULT_MODE = "BFS"

    def __init__(self, mode=DEFAULT_MODE):
         self.mode = mode


    def generatePath(self, maze,mode=DEFAULT_MODE):
        if mode == "BFS":
            return self.BFS(maze)


    def BFS(self,maze):

        matrix = maze.matrix
        start = maze.start
        end = maze.end

        visited = set()
        frontier = deque([[start]])

        while frontier:
            current_path = frontier.popleft()
            current = current_path[-1]


            if current == end:
                return current_path

            if current in visited:
                continue

            visited.add(current)
            neighbors = self.checkForNeighbors(current,matrix)


            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = current_path.copy()
                    new_path.append(neighbor)

                    frontier.append(new_path)




        return []



    def checkForNeighbors(self, pos, matrix):

            neighbors = []
            size = len(matrix)

            # oben
            if pos[0] > 0 and not matrix[pos[0] - 1][pos[1]] == maze.Maze.VALUE_WALL:
                neighbors.append((pos[0] - 1, pos[1]))

            # unten
            if pos[0] < size - 1 and not matrix[pos[0] + 1][pos[1]] == maze.Maze.VALUE_WALL:
                neighbors.append((pos[0] + 1, pos[1]))

            # links
            if pos[1] > 0 and not matrix[pos[0]][pos[1] - 1] == maze.Maze.VALUE_WALL:
                neighbors.append((pos[0], pos[1] - 1))

            # rechts
            if pos[1] < size - 1 and not matrix[pos[0]][pos[1] + 1] == maze.Maze.VALUE_WALL:
                neighbors.append((pos[0], pos[1] + 1))

            return neighbors








