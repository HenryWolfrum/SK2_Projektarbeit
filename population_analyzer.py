import matplotlib.pyplot as plt
import maze
import population_manager
import generation_data

class PopulationAnalyzer:

    def __init__(self):
        self.max_fitnesses = []
        self.average_fitnesses = []
        self.min_fitnesses = []

    def update(self,data):
        self.max_fitnesses.append(data.max_fitness)
        self.average_fitnesses.append(data.average_fitness)
        self.min_fitnesses.append(data.min_fitness)


    def plot_fitness_convergence(self):

        plt.plot(self.max_fitnesses,label="Max Fitness")
        plt.plot(self.average_fitnesses,label="Average Fitness")
        plt.plot(self.min_fitnesses,label="Min Fitness")

        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.show()

