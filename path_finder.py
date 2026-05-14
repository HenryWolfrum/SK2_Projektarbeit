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
            neighbors = maze.checkForNeighbors(current,1,maze.VALUE_WALL)


            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = current_path.copy()
                    new_path.append(neighbor)

                    frontier.append(new_path)


        return []








