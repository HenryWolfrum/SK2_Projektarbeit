import fitness_evaluator
import maze
import maze_generator
import maze_generator as mg
import maze_renderer
import path_finder
import maze_renderer as mr
import genetic_operator
import population_manager as pm
import population_analyzer as ap

def testPopulation():


    testAnalyzer = ap.PopulationAnalyzer()
    popM=pm.PopulationManager(testAnalyzer,25,"RANDOM",100,"IMPROVED")
    popM.runPopulation(200)

    testAnalyzer.plot_analysis()


#Programmeinstiegspunkt
if __name__ == '__main__':
    testPopulation()

    while True:
        pass



