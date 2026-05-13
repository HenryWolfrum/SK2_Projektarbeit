import genetic_operator
import maze_generator
import maze
import fitness_evaluator
import random
import maze_renderer
import path_finder


class PopulationManager:

    DEFAULT_POPULATION_SIZE = 100
    DEFAULT_SELECTION_MODE = "TOURNAMENT"

    MAX_GENERATION=100

    MUTATION_PROB = 0.1

    REPRODUCTION_SHARE = 0.8

    def __init__(self,size_maze,generating_mode,size_pop=DEFAULT_POPULATION_SIZE):
        self.size_pop = size_pop
        self.size_maze = size_maze
        self.generating_mode = generating_mode

        self.population = []


    def initializePopulation(self):

        for i in range(self.size_pop):
            genome = maze_generator.MazeGenerator().generateMaze(self.size_maze,self.generating_mode)
            self.population.append(genome)


    def runPopulation(self,generationCount=MAX_GENERATION):

        self.initializePopulation()



        generation = 1

        while generation<generationCount:
            #Bewerten
            self.gradePopulation()

            # Informationen ausgeben
            self.getInformationOnPopulation(generation)

            #Auswählen
            selected=self.selectNextPopulation()

            #Rekombinieren
            self.recombineSelected(selected)

            #Mutieren
            self.mutateSelected(selected)

            #Aktualisieren
            self.updatePopulation(selected)

            #Generation erhöhen
            generation += 1


    def gradePopulation(self):
        fitnessEv = fitness_evaluator.FitnessEvaluator()

        for i in range(self.size_pop):

            fitness=fitnessEv.calcFitness(self.population[i])

            self.population[i].setFitness(fitness)


    def selectNextPopulation(self,mode=DEFAULT_SELECTION_MODE):

        return self.tournamentSelection()


    #Teilmengenbildung und Auswahl des fittesten Genoms
    def tournamentSelection(self):

        selected=[]

        for i in range(round(self.size_pop*self.REPRODUCTION_SHARE)):

            #Wähle Teilmenge
            subset_size = random.randint(self.size_pop//6,self.size_pop//5)

            #Subset
            subset=random.sample(self.population,subset_size)

            fittestGenome = None

            for j in range(subset_size):
                randomGenome = subset[j]

                if fittestGenome == None:
                    fittestGenome = randomGenome

                elif randomGenome.fitness>fittestGenome.fitness:
                    fittestGenome = randomGenome


            selected.append(fittestGenome)



        return selected

    #Rekombination der ausgewählten Individuen
    def recombineSelected(self,selected):

        while(len(selected)<self.size_pop):

            #Zufällige Elternwahl
            parent1 = selected[random.randint(0,len(selected)-1)]
            parent2 = selected[random.randint(0,len(selected)-1)]

            #Kinder erzeugen
            children = genetic_operator.GeneticOperator().crossover(parent1,parent2)

            #Kinder in selected aufnehmen
            selected.append(children[0])
            selected.append(children[1])

    #Ausgewählte neue Population zufällig mutieren lassen
    def mutateSelected(self,selected):

        for i in range(len(selected)):
            if random.random() < self.MUTATION_PROB:
                genetic_operator.GeneticOperator().mutate(selected[i])

    #Aktualisiert die Population
    def updatePopulation(self,selected):
        self.population = selected

    #Gibt Informationen über Population aus
    def getInformationOnPopulation(self,generation):

        fittest=self.population[0]
        weakest=self.population[0]

        maxFitness=self.population[0].fitness
        minFitness=self.population[0].fitness

        sumFintess=0
        averageFitness=0

        for i in range(self.size_pop):

            if self.population[i].fitness>maxFitness:
                maxFitness=self.population[i].fitness
                fittest=self.population[i]
            elif self.population[i].fitness<minFitness:
                minFitness=self.population[i].fitness
                weakest=self.population[i]

            sumFintess=sumFintess + self.population[i].fitness

        averageFitness=sumFintess/self.size_pop

        print("Generation:",generation,"Max:",maxFitness,"Min:",minFitness,"Average:",averageFitness)

        if fittest != None and weakest != None:
            print("")
            maze_renderer.MazeRenderer().renderPathInMaze(fittest, path_finder.PathFinder().generatePath(fittest))
            print("")
            maze_renderer.MazeRenderer().renderPathInMaze(weakest, path_finder.PathFinder().generatePath(weakest))

    #Gibt die aktuelle Population zurück
    def getPopulation(self):
        return self.population