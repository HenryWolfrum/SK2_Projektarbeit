import fitness_evaluator
import maze
import random
import maze_renderer
import time

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

        self.duration = 0

        self.solved = False

    # Spiel-Hauptschleife
    def start(self, coin_count):
        # Münzen auf Maze verteilen
        self.distribute_coins(coin_count)

        # Solange Spiel nicht gelöst
        #Timer starten
        start_time = time.time()
        while not self.solved:
            # Agent macht Zug
            self.do_move(self.agent)
            # Überprüfe ob Spiel gelöst
            self.checkSolved()

        #Timer beenden
        end_time = time.time()
        self.duration = end_time - start_time

    # Verteilt die Münzen am Anfang des Spiels (in nur erreichbare Teile)
    def distribute_coins(self, count):
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

        if action in legal:
            self.agent_pos = action
            self.path_history.append(action)
            self.checkForCoin(self.agent_pos)
        else:
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
            if 0 <= nx < len(self.maze.matrix) and 0 <= ny < len(self.maze.matrix[0]):
                if self.maze.matrix[nx][ny] != maze.Maze.VALUE_WALL:
                    legal.append((nx, ny))

        return legal

    # Überprüft ob das Spiel zu Ende ist
    def checkSolved(self):
        if len(self.coins_pos) == 0 and self.agent_pos == self.maze.end:
            self.solved = True

    def drawGame(self):
        maze_renderer.MazeRenderer().renderAgentPathAnimated(self.maze, self.path_history,self.coins_pos_clone)

    def evaluateSolution(self):

        schritte = len(self.path_history)
        rechenzeit = self.duration


        maze_fitness =  fitness_evaluator.FitnessEvaluator().calcFitness(self.maze)


        weight_time = 100.0


        if schritte == 0:
            agent_score = 0
        else:

            agent_score = (maze_fitness * 1000) / (schritte + (rechenzeit * weight_time))


        print("\n" + "=" * 40)
        print("         EVALUATION ERGEBNIS")
        print("=" * 40)
        print(f" Labyrinth-Schwierigkeit (Fitness): {maze_fitness:.2f}")
        print(f" Benötigte Schritte:               {schritte}")
        print(f" Reine Rechenzeit:                 {rechenzeit:.4f} Sekunden")
        print("-" * 40)
        print(f" FINALER AGENTEN-SCORE:            {agent_score:.2f}")
        print("=" * 40 + "\n")

        input("[INFO] Drücke ENTER um die Animation zu starten...")
        self.drawGame()

        return agent_score

