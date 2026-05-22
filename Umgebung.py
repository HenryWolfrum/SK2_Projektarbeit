class Umgebung:
    def __init__(self, maze, agent, n):
        self.maze = maze
        self.agent = agent
        self.coin_count= 0
        self.coin_pos=[]
        self.path_history=[]

        MOVE_RIGHT="right"
        MOVE_LEFT="left"
        MOVE_UP="up"
        MOVE_DOWN="down"

        self.actions=[self.MOVE_RIGHT, self.MOVE_LEFT, self.MOVE_UP, self.MOVE_DOWN]
        self.solved = False

        def start(self,maze,agent, n):
            while not self.solved:
                self.do_move(self.agent)

        def do_move(self, agent):
            actions= agent.setAction(self, self.setInput(), self.setActions())

        def setInput(self):
            #return Zustand von Spiel
            return {
                "agent_pos": self.agent.pos,
                "coin_pos": self.coinPos,
                "coin_count": self.coin_count,
                "path_history": self.path_history,
            }

        def setActions(self):
            #wählt legale Züge
            x,y =self.agent.pos #aktuelle Position des Agenten
            legal=[]
            moves ={
                self.MOVE_RIGHT: (x+1,y),
                self.MOVE_LEFT: (x-1,y),
                self.MOVE_UP: (x,y-1),
                self.MOVE_DOWN: (x,y+1),
            } #Nachbarfelder

            for action, (nx,ny) in (moves.items()):
                if 0<= ny < len(self.maze) and 0<= nx < len(self.maze[0]):  #ist das feld im labyrinth
                    if self.maze[ny][nx] != 1: #ist es keine Wand
                        legal.append(action)
            return legal

        def checkSolved(self):
            if len(self.coinpos)==0 and self.agent.pos==self.maze.endPos:
                self.solved = True
