import maze_generator
import fitness_evaluator
import matplotlib.pyplot as plt

class AlgorithmComparer:

    DEFAULT_EXPERIMENT_RUNS = 30
    DEFAULT_SAMPLE_SIZE = 100

    DEFAULT_COMPARE_SET = []

    DEFAULT_COMPARE_FUNCTION="IMPROVED"

    def __init__(self,experiment_runs=DEFAULT_EXPERIMENT_RUNS,sample_size=DEFAULT_SAMPLE_SIZE,compare_set=DEFAULT_COMPARE_SET,compare_function=DEFAULT_COMPARE_FUNCTION):
        self.experiment_runs = experiment_runs
        self.sample_size = sample_size
        self.compare_set = compare_set
        self.compare_function = compare_function
        self.maze_generator = maze_generator.MazeGenerator()
        self.fitness_evaluator = fitness_evaluator.FitnessEvaluator()

        self.DEFAULT_COMPARE_SET=[self.maze_generator.MODE_RANDOM,self.maze_generator.MODE_RANDOM_DFS,self.maze_generator.MODE_GENETIC_ALGORITHM]
        self.DEFAULT_COMPARE_FUNCTION=self.fitness_evaluator.FUNCTION_IMPROVED

    #Vergleicht Algorithmen im compare_set, wobei experiment_runs Durchläufe mit jeweils sample_size generierten Mazes durchgeführt werden. Das Ergebnis sind die besten erreichten fitness Werte
    def compareSet(self):
        compare_data={}

        for algorithm in self.compare_set:
            compare_data[algorithm]=[]

        for _ in range(self.experiment_runs):
            run_result=self.doRun()

            for i in range(len(run_result)):
                algorithm_result=run_result[i]
                algorithm=algorithm_result[0]
                fitness=algorithm_result[1]

                compare_data[algorithm].append(fitness)

        return compare_data

    #Führt einen Durchlauf in jeder Algorithmus Kategorie durch
    def doRun(self):
        print("RUN")
        run_results = []
        for algorithm in self.compare_set:
                if algorithm==self.maze_generator.MODE_GENETIC_ALGORITHM:
                    best_maze = self.maze_generator.generateMaze(self.maze_generator.DEFAULT_SIZE,algorithm)
                    fitness = self.fitness_evaluator.calcFitness(best_maze,self.compare_function)
                    run_results.append((algorithm,fitness))
                else:
                    run_results.append((algorithm, self.evaluateSample(algorithm, self.sample_size)))


        return run_results


    #Wertet die beste Fitness von sample_size generierten Labyrinthen
    def evaluateSample(self,algorithm,sample_size):
        sample_fitness = []
        for i in range(sample_size):
            sample_fitness.append(self.evaluateOne(algorithm))

        return max(sample_fitness)

    #Wertet die Fitness eines mit algorithm generierten Labyrinth aus
    def evaluateOne(self,algorithm):
           maze = self.maze_generator.generateMaze(self.maze_generator.DEFAULT_SIZE,algorithm)

           fitness = self.fitness_evaluator.calcFitness(maze,self.compare_function)

           return fitness

    def plot_compare_results(self,compare_data):
        data = list(compare_data.values())
        labels = list(compare_data.keys())

        plt.boxplot(data, tick_labels=labels)

        plt.axhline(y=fitness_evaluator.FitnessEvaluator().maximum_fitness, linestyle="--")

        plt.ylabel("Fitness")
        plt.xlabel("Algorithm")
        plt.title("Algorithm Comparison")

        plt.show()
