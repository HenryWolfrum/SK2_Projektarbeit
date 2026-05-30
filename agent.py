from abc import ABC, abstractmethod
from collections import deque
import heapq
from collections import deque


#Abstrake Oberklasse
class Agent(ABC):

    @abstractmethod
    def selectAction(self, input, actions):
        pass


#Greedy Agent
class GreedyAgent(Agent):

    def __init__(self):
        self.goal       = None
        self.visited    = set()
        self.path_stack = []

    #Wählt eine Aktion nach Greedy Prinzip
    def selectAction(self, input, actions):
        #Input
        coins_pos           = input["coins_pos"]
        agent_pos           = input["agent_pos"]
        end_pos             = input["end_pos"]
        maze                = input["maze"]
        collected_last_move = input["coin_collected_last_move"] == True

        #Muss ein neues Ziel ermittelt werden?
        if collected_last_move or self.goal is None or agent_pos == self.goal:
            #Neues Ziel mit Heursitik ermitteln und Rest zurücksetzen
            targets         = list(coins_pos) if coins_pos else [end_pos]
            self.goal       = self.nearest(agent_pos, targets)
            self.visited    = set()
            self.path_stack = [agent_pos]

        #Jetzige Position als besucht markieren
        self.visited.add(agent_pos)

        #Überprüfen der unbesuchten Nachbarn
        neighbors = maze.checkForNeighbors(agent_pos, 1, maze.VALUE_WALL)
        unvisited = [n for n in neighbors if n not in self.visited]

        #Gehe zum am besten bewerteten Nachbarn
        if unvisited:
            best = self.nearest(self.goal, unvisited)
            self.path_stack.append(best)
            return best

        #Bei keinen unbesuchten Nachbarn gehe auf das Feld wo du herkamst
        if len(self.path_stack) > 1:
            self.path_stack.pop()
            return self.path_stack[-1]

        return None


    #Heuristik Methode (euklidische Distanz)
    def nearest(self, origin, positions):
        best = None
        best_dist = float("inf")

        for pos in positions:
            dist = ((pos[0] - origin[0]) ** 2 +
                    (pos[1] - origin[1]) ** 2) ** 0.5

            if dist < best_dist:
                best_dist = dist
                best = pos

        return best
