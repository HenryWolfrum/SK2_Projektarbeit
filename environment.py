import maze
import random

class Environment:


    def __init__(self, maze, agent):
        self.maze = maze
        self.agent = agent

        # einzige Positionsquelle
        self.agent_pos = maze.startPos

        self.coin_count = 0
        self.coins_pos = []
        self.path_history = []

        self.coin_collected_last_move = False


        self.solved = False

    #Spiel Hauptschleife
    def start(self, coin_count):
        #Münzen auf Maze verteilen
        self.distribute_coins(coin_count)

        #Solange Spiel nicht gelöst
        while not self.solved:
            #Agent macht Zug
            self.do_move(self.agent)
            #Überprüfe ob Spiel gelöst
            self.checkSolved()

    #Verteilt die Münzen am Anfang des Spiels
    def distribute_coins(self, count):

        free_space = set()

        rows = len(self.maze.matrix)
        cols = len(self.maze.matrix[0])

        for i in range(rows):
            for j in range(cols):
                if self.maze.matrix[i][j] == maze.Maze.VALUE_EMPTY:
                    free_space.add((i, j))

        # Falls weniger freie Felder als coins existieren
        count = min(count, len(free_space))

        self.coins_pos = random.sample(list(free_space), count)

    #Agent macht Zug
    def do_move(self, agent):
        action = agent.selectAction(self.setInput(), self.setActions())

        #Wenn Aktion legal war (Normalfall immer)
        if action in self.setActions():
            #Agenten verschieben
            self.agent_pos = action
            self.path_history.append(action)

            #Überprüfen ob er auf einer Münze ist
            self.checkForCoin(self.agent_pos)


    #Entfernt Münze wenn Agent auf einer steht und markiert den bool für nächsten Zug
    def checkForCoin(self, pos):
        if pos in self.coins_pos:
            self.coins_pos.remove(pos)
            self.coin_collected_last_move = True
        else:
            self.coin_collected_last_move = False

    #erzeugt den Input für den Agent
    def setInput(self):
        return {
            "agent_pos": self.agent_pos,
            "end_pos": self.maze.endPos,
            "coins_pos": self.coins_pos,
            "coin_collected_last_move": self.coin_collected_last_move,
            "maze": self.maze,
            "path_history": self.path_history,
        }

    #Erzeugt die Menge legaler Aktionen
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
            if 0 <= ny < len(self.maze.matrix) and 0 <= nx < len(self.maze.matrix[0]):
                if self.maze.matrix[ny][nx] != maze.Maze.VALUE_WALL:
                    legal.append((nx, ny))

        return legal

    #Überprüft ob das Spiel zu Ende ist
    def checkSolved(self):
        if len(self.coins_pos) == 0 and self.agent_pos == self.maze.endPos:
            self.solved = True