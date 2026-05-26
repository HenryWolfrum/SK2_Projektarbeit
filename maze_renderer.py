import time
import maze


class MazeRenderer:

    RENDER_WALL             = "\033[40m  \033[0m"
    RENDER_EMPTY            = "\033[47m  \033[0m"
    RENDER_ERROR            = "\033[35m??\033[0m"
    RENDER_START            = "\033[41;1mST\033[0m"
    RENDER_END              = "\033[42;1mEX\033[0m"

    RENDER_AGENT            = "\033[46;1m◆ \033[0m"
    RENDER_PATH_ARROW       = "\033[45;1m{} \033[0m"
    RENDER_COIN             = "\033[103;1m● \033[0m"

    LEGEND = (
        " \033[41;1mST\033[0m Start   "
        "\033[42;1mEX\033[0m Exit   "
        "\033[46;1m◆ \033[0m Agent   "
        "\033[45;1m→ \033[0m Pfad   "
        "\033[103;1m● \033[0m Münze   "
        "\033[40m  \033[0m Wand   "
        "\033[47m  \033[0m Frei"
    )

    #Zeichnet das Maze mit (0,0) unten links
    def renderMaze(self, maze_obj):
        matrix = maze_obj.matrix
        for j in range(len(matrix) - 1, -1, -1):
            print("")
            for i in range(len(matrix)):
                print(self.getColorForValue(matrix[i][j]), end="")
        print("")
        print(self.LEGEND)
        print("")

    #Zeichnet Maze mit Pfad
    def renderPathInMaze(self, maze_obj, path):
        matrix   = maze_obj.matrix
        path_set = set(path)

        for j in range(len(matrix) - 1, -1, -1):
            print("")
            for i in range(len(matrix)):
                pos = (i, j)
                if pos in path_set and pos != maze_obj.start and pos != maze_obj.end:
                    print(self.RENDER_PATH_ARROW.format("·"), end="")
                else:
                    print(self.getColorForValue(matrix[i][j]), end="")
        print("")
        print(self.LEGEND)
        print("")

    def renderAgentPathInMaze(self, maze_obj, path_history, coins_pos, collected_coins_pos=None):
        if not path_history:
            self.renderMaze(maze_obj)
            return

        matrix    = maze_obj.matrix
        path_set  = set(path_history)
        last_pos  = path_history[-1]
        remaining = set(coins_pos) if coins_pos else set()
        collected = set(collected_coins_pos) if collected_coins_pos else set()

        #Bewegungsrichtung berechnen
        directions = {}
        for idx in range(len(path_history) - 1):
            cur = path_history[idx]
            nxt = path_history[idx + 1]
            dx = nxt[0] - cur[0]
            dy = nxt[1] - cur[1]

            if dx > 0:
                arrow = "→"
            elif dx < 0:
                arrow = "←"
            elif dy > 0:
                arrow = "↑"
            elif dy < 0:
                arrow = "↓"
            else:
                arrow = "·"

            directions[cur] = arrow

        for j in range(len(matrix) - 1, -1, -1):
            print("")
            for i in range(len(matrix)):
                pos = (i, j)

                # 1. Höchste Priorität: Start und Ende fest verankern
                if pos == maze_obj.start:
                    print(self.RENDER_START, end="")
                elif pos == maze_obj.end:
                    print(self.RENDER_END, end="")

                # 2. Zweite Priorität: Ist hier aktuell der Agent?
                elif pos == last_pos:
                    # Falls der Agent AUF einer eingesammelten Münze steht,
                    # könnte man hier sogar ein spezielles Symbol nutzen, falls gewünscht.
                    print(self.RENDER_AGENT, end="")

                # 3. Dritte Priorität: Wurde hier jemals eine Münze eingesammelt?
                elif collected and pos in collected:
                    print(self.RENDER_COIN_COLLECTED, end="")

                # 4. Vierte Priorität: Ist der Agent hier einfach nur langgelaufen?
                elif pos in path_set:
                    arrow = directions.get(pos, "·")
                    print(self.RENDER_PATH_ARROW.format(arrow), end="")

                # 5. Fünfte Priorität: Liegt hier noch eine unberührte Münze?
                elif pos in remaining:
                    print(self.RENDER_COIN, end="")

                # 6. Letzte Priorität: Einfach nur Wand oder Boden
                else:
                    print(self.getColorForValue(matrix[i][j]), end="")

        print("")
        print(self.LEGEND)

    #Zeichnet immer nur einen Teil des Verlaufs für Animationseffekt
    def renderAgentPathAnimated(self, maze_obj, path_history, coins_pos, collected_coins_pos=None, delay=0.075):
        matrix      = maze_obj.matrix
        maze_height = len(matrix)

        lines       = maze_height + 2

        for step in range(1, len(path_history) + 1):
            if step > 1:
                print(f"\033[{lines}A", end="", flush=True)

            self.renderAgentPathInMaze(maze_obj, path_history[:step], coins_pos, collected_coins_pos)
            time.sleep(delay)

    #Übersetzt die Werte in festgelegte Farben
    def getColorForValue(self, value):
        if   value == maze.Maze.VALUE_START: return self.RENDER_START
        elif value == maze.Maze.VALUE_END:   return self.RENDER_END
        elif value == maze.Maze.VALUE_EMPTY: return self.RENDER_EMPTY
        elif value == maze.Maze.VALUE_WALL:  return self.RENDER_WALL
        else:                                return self.RENDER_ERROR