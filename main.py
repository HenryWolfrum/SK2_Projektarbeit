import fitness_evaluator
import maze
import maze_generator
import maze_generator as mg
import maze_renderer
import path_finder
import maze_renderer as mr
import genetic_operator
import population_manager as pm

def testPopulation():

    popM=pm.PopulationManager(25,"RANDOM",100,"IMPROVED")
    popM.runPopulation(100)




#Programmeinstiegspunkt
if __name__ == '__main__':

    testPopulation()

    while True:
        pass



