import genetic_operator
import maze_generator
import fitness_evaluator
import random
import generation_data
import time

class PopulationManager:

    DEFAULT_POPULATION_SIZE = 100

    #Standard Selektionsalgorithmus
    DEFAULT_SELECTION_MODE = "TOURNAMENT"

    DEFAULT_GENERATING_MODE = "RANDOM"

    MAX_GENERATION=200

    MUTATION_PROB = 0.3

    #Maximale Anzahl an Zellmutationen pro Mutation
    MUTATION_CELLS_MAX=0.06
    #Minimale Anzahl an Zellmutationen pro Mutation
    MUTATION_CELLS_MIN=0.03

    #Anteil der Population der selektiert wird für die nächste Generation
    SELECTION_SHARE = 0.25

    #Größenanteil einer Teilmenge bei Turnierselektion
    TOURNAMENT_SHARE = 0.03

    def __init__(self,size_maze,generating_mode=DEFAULT_GENERATING_MODE,size_pop=DEFAULT_POPULATION_SIZE,fitness_function=None):
        self.size_pop = size_pop
        self.size_maze = size_maze
        self.generating_mode = generating_mode

        if fitness_function == None:
            self.fitness_function=fitness_evaluator.FitnessEvaluator().DEFAULT_FUNCTION
        else:
            self.fitness_function = fitness_function

        self.population = []
        self.observers = []

        self.maze_generator=maze_generator.MazeGenerator()
        self.fitness_evaluator=fitness_evaluator.FitnessEvaluator()


    #Fügt einen Beobachter (wie Analysetool) hinzu
    def addObserver(self,observer):
        self.observers.append(observer)

    #Benachrichtig die Beobachter für Änderungen
    def notifyObservers(self,data):
        for observer in self.observers:
            observer.update(data)

    #Generiert eine Startpopulation
    def initializePopulation(self):

        for i in range(self.size_pop):
            genome = self.maze_generator.generateMaze(self.size_maze,self.generating_mode)
            self.population.append(genome)

    #Hauptschleife des genetischen Algorithmus
    def runPopulation(self,generationCount=MAX_GENERATION):

        self.initializePopulation()

        generation = 1

        while generation < generationCount:

            self.gradePopulation()


            self.createGenerationDataPackage(generation)


            selected = self.selectNextPopulation()


            self.recombineSelected(selected)


            self.mutateSelected(selected)


            self.updatePopulation(selected)

            generation += 1



    def gradePopulation(self):

        for i in range(self.size_pop):

            fitness=self.fitness_evaluator.calcFitness(self.population[i],self.fitness_function)

            self.population[i].setFitness(fitness)


    def selectNextPopulation(self,mode=DEFAULT_SELECTION_MODE):

        return self.tournamentSelection()


    #Teilmengenbildung und Auswahl des fittesten Genoms
    def tournamentSelection(self):
        selected = []
        alreadySelected = set()

        for i in range(round(self.size_pop * self.SELECTION_SHARE)):
            subset_size = round(self.size_pop * self.TOURNAMENT_SHARE)
            subset = random.sample(self.population, subset_size)

            fittestGenome = None
            for j in range(subset_size):
                randomGenome = subset[j]
                if fittestGenome is None:
                    fittestGenome = randomGenome
                elif randomGenome.fitness > fittestGenome.fitness:
                    fittestGenome = randomGenome

            # Klon vermeiden
            if id(fittestGenome) not in alreadySelected:
                selected.append(fittestGenome)
                alreadySelected.add(id(fittestGenome))

        return selected
    #Rekombination der ausgewählten Individuen
    def recombineSelected(self, selected):
        while len(selected) < self.size_pop:
            parent1 = selected[random.randint(0, len(selected) - 1)]
            parent2 = selected[random.randint(0, len(selected) - 1)]

            children = genetic_operator.GeneticOperator().crossover(parent1, parent2)

            selected.append(children[0])
            # Bug-Fix: nicht überschießen
            if len(selected) < self.size_pop:
                selected.append(children[1])
    #Ausgewählte Individuen mutieren
    def mutateSelected(self,selected):

        for i in range(len(selected)):
            if random.random() < self.MUTATION_PROB:
                totalCells = len(selected[i].matrix)**2
                mutateCount = round(random.uniform(self.MUTATION_CELLS_MIN,self.MUTATION_CELLS_MAX)*totalCells)
                genetic_operator.GeneticOperator().mutate(selected[i],mutateCount)

    #Aktualisieren der Population
    def updatePopulation(self, selected):
        # Bestes Individuum der alten Population immer übernehmen
        bestMaze = self.population[0]
        for i in range(self.size_pop):
            if self.population[i].fitness > bestMaze.fitness:
                bestMaze = self.population[i]
        selected[-1] = bestMaze
        self.population = selected

    #Erstellt ein Informationspaket für die Generation
    def createGenerationDataPackage(self,generation):

        maxFitness = self.population[0].fitness
        minFitness = self.population[0].fitness

        fittest_maze = self.population[0]
        weakest_maze = self.population[0]

        sumFintess = 0

        for i in range(self.size_pop):

            if self.population[i].fitness > maxFitness:
                maxFitness = self.population[i].fitness
                fittest_maze=self.population[i]
            elif self.population[i].fitness < minFitness:
                minFitness = self.population[i].fitness
                weakest_maze=self.population[i]

            sumFintess = sumFintess + self.population[i].fitness

        averageFitness = sumFintess / self.size_pop

        #Anteil an unterschiedlichen Labyrinth-strukturen berechnen
        unique_ratio = self.calcUniqueMazeRatio()

        #Daten an Observer geben
        package=generation_data.GenerationData(generation,maxFitness,averageFitness,minFitness,fittest_maze,weakest_maze,unique_ratio)



        self.notifyObservers(package)

    def calcUniqueMazeRatio(self):

        unique = set()

        for maze in self.population:
            hashable_matrix = tuple(tuple(row)for row in maze.matrix)

            unique.add(hashable_matrix)

        return len(unique) / self.size_pop


    #Gibt die aktuelle Population zurück
    def getPopulation(self):
        return self.population
