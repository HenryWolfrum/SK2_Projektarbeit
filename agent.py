from abc import ABC, abstractmethod
from collections import deque


class Agent(ABC):

    @abstractmethod
    def selectAction(self, input, actions):
        pass


class GreedyAgent(Agent):

    def __init__(self):
        self.last_followed_path = deque()

    def selectAction(self, input, actions):
        collected_last_move = input["coin_collected_last_move"] == True

        coins_pos = input["coins_pos"]
        agent_pos = input["agent_pos"]
        end_pos = input["end_pos"]
        maze = input["maze"]

        # 1. Ziel: Exit
        if len(coins_pos) == 0:
            if collected_last_move or len(self.last_followed_path) == 0:
                path = self.calcNewPath([end_pos], agent_pos, maze)
                self.last_followed_path = deque(path)

            return self.getNextAction()

        # 2. Ziel: Coins
        if collected_last_move or len(self.last_followed_path) == 0:
            path = self.calcNewPath(coins_pos, agent_pos, maze)
            self.last_followed_path = deque(path)

        return self.getNextAction()

    def calcNewPath(self, goals_pos, start_pos, maze):
        visited = set()
        frontier = deque([(start_pos, [start_pos])])

        while frontier:
            current, path = frontier.popleft()

            if current in goals_pos:
                return path

            if current in visited:
                continue

            visited.add(current)

            neighbors = maze.checkForNeighbors(current, 1, maze.VALUE_WALL)

            for neighbor in neighbors:
                if neighbor not in visited:
                    frontier.append((neighbor, path + [neighbor]))

        return []

    def getNextAction(self):
        if not self.last_followed_path:
            return None

        # Aktuelle Position (Startposition) entfernen
        self.last_followed_path.popleft()

        if not self.last_followed_path:
            return None

        return self.last_followed_path[0]