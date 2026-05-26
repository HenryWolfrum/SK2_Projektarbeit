import agent
import maze
from collections import deque


class Environment:

    MOVE_RIGHT = "right"
    MOVE_LEFT = "left"
    MOVE_UP = "up"
    MOVE_DOWN = "down"

    def __init__(self, maze, agent, n):
        self.maze = maze
        self.agent = agent

        # einzige Positionsquelle
        self.agent_pos = maze.startPos

        self.coin_count = 0
        self.coins_pos = []
        self.path_history = []

        self.coin_collected_last_move = False

        self.actions = [
            self.MOVE_RIGHT,
            self.MOVE_LEFT,
            self.MOVE_UP,
            self.MOVE_DOWN
        ]

        self.solved = False

    #Spiel Hauptschleife
    def start(self, maze, agent, coin_count):
        while not self.solved:
            self.do_move(self.agent)
            self.checkSolved()



    def do_move(self, agent):
        action = agent.selectAction(self, self.setInput(), self.setActions())

        if action in self.setActions():
            self.agent_pos = action
            self.path_history.append(action)

            self.checkForCoin(self.agent_pos)

    def checkForCoin(self, pos):
        if pos in self.coins_pos:
            self.coins_pos.remove(pos)
            self.coin_collected_last_move = True
        else:
            self.coin_collected_last_move = False

    def setInput(self):
        return {
            "agent_pos": self.agent_pos,
            "end_pos": self.maze.endPos,
            "coins_pos": self.coins_pos,
            "coin_collected_last_move": self.coin_collected_last_move,
            "maze": self.maze,
            "path_history": self.path_history,
        }

    def setActions(self):
        x, y = self.agent_pos

        moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

        legal = []

        for nx, ny in moves:
            if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):
                if self.maze[ny][nx] != maze.Maze.VALUE_WALL:
                    legal.append((nx, ny))

        return legal

    def checkSolved(self):
        if len(self.coins_pos) == 0 and self.agent_pos == self.maze.endPos:
            self.solved = True