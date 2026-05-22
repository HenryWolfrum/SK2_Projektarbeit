class Agent:

    def selectAction(selfself, input, actions):
        raise NotImplementedError("selectAction muss implementiert werden")
        #jede klasse muss diese Methode selbst implementieren weil raise NotImplementedError eine abstrakte Methode ist


    def move_right(self):
        self.pos=(self.pos[0]+1,self.pos[1])

    def move_left(self):
        self.pos=(self.pos[0]-1,self.pos[1])

    def move_up(self):
        self.pos=(self.pos[0],self.pos[1]-1)

    def move_down(self):
        self.pos=(self.pos[0],self.pos[1]+1)



class GreedyAgent(Agent):

    def selectAction(self, input, actions): #selectActions vererbt
        #Gierige Suche
        return actions[0]
