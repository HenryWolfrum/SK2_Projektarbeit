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
        # Greedy: Ziel wählen + BFS Pfad nutzen

        collected_last_move = input["coin_collected_last_move"] == True

        coins_pos = input["coins_pos"]
        agent_pos = input["agent_pos"]
        end_pos = input["end_pos"]
        maze = input["maze"]

        # 1. Wenn alle Münzen weg sind → Ziel ist Exit
        if len(coins_pos) == 0:

            # neuer Pfad nur wenn vorher etwas abgeschlossen wurde oder noch keiner existiert
            if collected_last_move or len(self.last_followed_path) == 0:
                path = self.calcNewPath([end_pos], agent_pos, maze)
                self.last_followed_path = deque(path)

            return self.getNextAction(actions)

        # 2. Wenn gerade eine Münze eingesammelt wurde → neues Ziel berechnen
        if collected_last_move or len(self.last_followed_path) == 0:
            path = self.calcNewPath(coins_pos, agent_pos, maze)
            self.last_followed_path = deque(path)

        # 3. Pfad weiter ablaufen
        return self.getNextAction(actions)

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

    def getNextAction(self, actions):

        if not self.last_followed_path:
            return None

        next_pos = self.last_followed_path.popleft()

        # Startposition nicht als Bewegung behandeln
        if next_pos not in actions:
            # falls inkonsistent → einfach ignorieren
            return None

        return next_pos