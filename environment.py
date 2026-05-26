import maze
import random
import maze_renderer

class Environment:

    def __init__(self, maze, agent):
        self.maze = maze
        self.agent = agent

        # Einzige Positionsquelle
        self.agent_pos = maze.start

        self.coin_count = 0
        self.coins_pos = []
        self.coins_pos_clone = []
        self.path_history = []

        self.coin_collected_last_move = False

        self.solved = False

    # Spiel-Hauptschleife
    def start(self, coin_count):
        # Münzen auf Maze verteilen
        self.distribute_coins(coin_count)

        # Solange Spiel nicht gelöst
        while not self.solved:
            # Agent macht Zug
            self.do_move(self.agent)
            # Überprüfe ob Spiel gelöst
            self.checkSolved()

    # Verteilt die Münzen am Anfang des Spiels
    def distribute_coins(self, count):
        # FIX: Nur erreichbare Felder per BFS vom Start aus verwenden,
        # damit Coins nie in abgetrennten Maze-Bereichen landen.
        reachable = set()
        frontier = [self.maze.start]
        visited = {self.maze.start}

        while frontier:
            current = frontier.pop()
            reachable.add(current)
            neighbors = self.maze.checkForNeighbors(current, 1, self.maze.VALUE_WALL)
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    frontier.append(nb)

        # Startposition und Endposition ausschließen
        reachable.discard(self.maze.start)
        reachable.discard(self.maze.end)

        # Falls weniger erreichbare Felder als Coins existieren
        count = min(count, len(reachable))

        self.coins_pos = random.sample(list(reachable), count)
        self.coins_pos_clone=self.coins_pos.copy()

    # Agent macht Zug
    def do_move(self, agent):
        legal = self.setActions()
        action = agent.selectAction(self.setInput(), legal)

        # FIX: Wenn Aktion legal ist, Agent bewegen
        if action in legal:
            self.agent_pos = action
            self.path_history.append(action)
            self.checkForCoin(self.agent_pos)
        else:
            # Pfad war ungültig → Agent-Pfad zurücksetzen, damit neu geplant wird
            print(f"[WARN] Ungültige Action {action} von Agent, legal wäre: {legal}")
            self.agent.last_followed_path.clear()

    # Entfernt Münze wenn Agent auf einer steht und setzt den Bool für nächsten Zug
    def checkForCoin(self, pos):
        if pos in self.coins_pos:
            self.coins_pos.remove(pos)
            self.coin_collected_last_move = True
        else:
            self.coin_collected_last_move = False

    # Erzeugt den Input für den Agent
    def setInput(self):
        return {
            "agent_pos": self.agent_pos,
            "end_pos": self.maze.end,
            "coins_pos": self.coins_pos,
            "coin_collected_last_move": self.coin_collected_last_move,
            "maze": self.maze,
            "path_history": self.path_history,
        }

    # Erzeugt die Menge legaler Aktionen
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
            # FIX: nx ist Zeile → gegen Zeilenanzahl prüfen
            #      ny ist Spalte → gegen Spaltenanzahl prüfen (war vorher vertauscht!)
            if 0 <= nx < len(self.maze.matrix) and 0 <= ny < len(self.maze.matrix[0]):
                if self.maze.matrix[nx][ny] != maze.Maze.VALUE_WALL:
                    legal.append((nx, ny))

        return legal

    # Überprüft ob das Spiel zu Ende ist
    def checkSolved(self):
        print("agent:", self.agent_pos, "end:", self.maze.end, "coins:", len(self.coins_pos))
        if len(self.coins_pos) == 0 and self.agent_pos == self.maze.end:
            self.solved = True

    def drawGame(self):
        maze_renderer.MazeRenderer().renderAgentPathAnimated(self.maze, self.path_history,self.coins_pos_clone)

    def evaluateSolution(self):
        pass
