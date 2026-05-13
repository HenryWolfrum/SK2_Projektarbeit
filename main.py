import fitness_evaluator
import maze_generator as mg
import maze_renderer
import path_finder
import maze_renderer as mr
import genetic_operator
import population_manager as pm

def testMethod():

    testPopM = pm.PopulationManager(25,"RANDOM")
    testPopM.runPopulation(100)
    pop=testPopM.getPopulation()



#Programmeinstiegspunkt
if __name__ == '__main__':

    testMethod()

    while True:
        pass



