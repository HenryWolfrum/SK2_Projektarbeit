import genetic_operator
import maze_generator
import fitness_evaluator
import random
import generation_data

class PopulationManager:

    DEFAULT_POPULATION_SIZE = 100

    #Standard Selektionsalgorithmus
    DEFAULT_SELECTION_MODE = "TOURNAMENT"

    DEFAULT_GENERATING_MODE = "RANDOM"

    DEFAULT_MAX_GENERATION=200

    DEFAULT_MUTATION_RATE = 0.4

    #Maximale Anzahl an Zellmutationen pro Mutation
    DEFAULT_MUTATION_CELLS_MAX=0.06
    #Minimale Anzahl an Zellmutationen pro Mutation
    DEFAULT_MUTATION_CELLS_MIN=0.08

    #Anteil der Population der selektiert wird für die nächste Generation
    DEFAULT_SURVIVOR_RATE = 0.3

    #Größenanteil einer Teilmenge bei Turnierselektion
    DEFAULT_TOURNAMENT_SIZE = 3

    DEFAULT_HYPERPARAMETERS={"mutation_rate":DEFAULT_MUTATION_RATE,
                             "survivor_rate":DEFAULT_SURVIVOR_RATE,
                             "tournament_size":DEFAULT_TOURNAMENT_SIZE}

    LOG_MODE_REDUCED = "REDUCED"
    LOG_MODE_FULL = "FULL"

    def __init__(self,size_maze,generating_mode=DEFAULT_GENERATING_MODE,size_pop=DEFAULT_POPULATION_SIZE,fitness_function=None,hyperparameters=None,log_info=False,log_mode=LOG_MODE_REDUCED):
        self.size_pop = size_pop
        self.size_maze = size_maze
        self.generating_mode = generating_mode
        self.elite = None


        if fitness_function is None:
            self.fitness_function=fitness_evaluator.FitnessEvaluator().DEFAULT_FUNCTION
        else:
            self.fitness_function = fitness_function

        if hyperparameters is None:
            self.hyperparameters=self.DEFAULT_HYPERPARAMETERS.copy()
        else:
            self.hyperparameters = hyperparameters.copy()

        self.log_info = log_info
        self.log_mode = log_mode

        self.population = []
        self.observers = []



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
            genome = maze_generator.MazeGenerator().generateMaze(self.size_maze,self.generating_mode)
            self.population.append(genome)

    #Hauptschleife des genetischen Algorithmus
    def runPopulation(self,max_generations=DEFAULT_MAX_GENERATION):

        self.initializePopulation()

        generation = 1

        while generation < max_generations:

            self.gradePopulation()

            self.createGenerationDataPackage(generation)

            selected = self.selectNextPopulation()

            self.recombineSelected(selected)

            self.mutateSelected(selected)

            self.updatePopulation(selected)


            #Generation erhöhen
            generation += 1



    def gradePopulation(self):
        fitness_ev = fitness_evaluator.FitnessEvaluator()

        for i in range(self.size_pop):

            fitness=fitness_ev.calcFitness(self.population[i],self.fitness_function)

            self.population[i].setFitness(fitness)


    def selectNextPopulation(self,mode=DEFAULT_SELECTION_MODE):

        tournament_selection = self.tournamentSelection()

        #Fittestes Individuum immer übernehmen
        fittest_individual=self.population[0]
        for i in range(self.size_pop):
            if self.population[i].fitness > fittest_individual.fitness:
                fittest_individual = self.population[i]

        self.elite=fittest_individual

        if len(tournament_selection)==len(self.population):
            tournament_selection[0]=fittest_individual
        else:
            tournament_selection.append(fittest_individual)

        return tournament_selection

    #Teilmengenbildung und Auswahl des fittesten Genoms
    def tournamentSelection(self):

        selected=[]

        for i in range(round(self.size_pop*self.hyperparameters["survivor_rate"])):

            #Wähle Teilmengengröße
            subset_size = self.hyperparameters["tournament_size"]

            #Teilmenge
            subset=random.sample(self.population,subset_size)

            fittest_individual = None

            for j in range(subset_size):
                random_individual = subset[j]

                if fittest_individual is None:
                    fittest_individual = random_individual

                elif random_individual.fitness>fittest_individual.fitness:
                    fittest_individual = random_individual


            selected.append(fittest_individual)



        return selected

    #Rekombination der ausgewählten Individuen
    def recombineSelected(self,selected):

        #Rekombinieren bis Population voll
        while len(selected)<self.size_pop:

            #Zufällige Elternwahl
            parent1 = selected[random.randint(0,len(selected)-1)]
            parent2 = selected[random.randint(0,len(selected)-1)]

            #Kinder erzeugen
            children = genetic_operator.GeneticOperator().crossover(parent1,parent2)

            selected.append(children[0])

            #Check ob zweites Kind noch rein passt
            if len(selected)<self.size_pop:
                selected.append(children[1])


    #Ausgewählte Individuen mutieren
    def mutateSelected(self,selected):

        for i in range(len(selected)):
            if selected[i]!=self.elite:
                if random.random() < self.hyperparameters["mutation_rate"]:
                    total_cells = len(selected[i].matrix)**2
                    mutate_count = round(random.uniform(self.DEFAULT_MUTATION_CELLS_MIN,self.DEFAULT_MUTATION_CELLS_MAX)*total_cells)
                    genetic_operator.GeneticOperator().mutate(selected[i],mutate_count)

    #Aktualisieren der Population
    def updatePopulation(self,selected):
        self.population = selected


    #Erstellt ein Informationspaket für die Generation
    def createGenerationDataPackage(self,generation):

        max_fitness = self.population[0].fitness
        min_fitness = self.population[0].fitness

        fittest_maze = self.population[0]
        weakest_maze = self.population[0]

        sum_fitness = 0

        for i in range(self.size_pop):

            if self.population[i].fitness > max_fitness:
                max_fitness = self.population[i].fitness
                fittest_maze=self.population[i]
            if self.population[i].fitness < min_fitness:
                min_fitness = self.population[i].fitness
                weakest_maze=self.population[i]

            sum_fitness = sum_fitness + self.population[i].fitness

        average_fitness = sum_fitness / self.size_pop

        #Anteil an unterschiedlichen Labyrinth-strukturen berechnen
        unique_ratio = self.calcUniqueMazeRatio()

        #Daten an Observer geben
        package=generation_data.GenerationData(generation,max_fitness,average_fitness,min_fitness,fittest_maze,weakest_maze,unique_ratio)

        if self.log_info:
            if self.log_mode == self.LOG_MODE_REDUCED:
                package.printReducedData()
            else:
                package.printFullData()


        self.notifyObservers(package)

    #Berechnet den Anteil an ungleichen Mazes
    def calcUniqueMazeRatio(self):

        unique = set()

        for maze in self.population:
            hashable_matrix = tuple(tuple(row)for row in maze.matrix)

            unique.add(hashable_matrix)

        return len(unique) / self.size_pop

