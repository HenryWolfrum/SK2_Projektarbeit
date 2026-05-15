import matplotlib.pyplot as plt
import maze
import population_manager

class PopulationAnalyzer:

    max_fitnesses = []
    average_fitnesses = []
    min_fitnesses = []

    def plot_analysis(self):

        plt.plot(self.max_fitnesses,label="Max Fitness")
        plt.plot(self.average_fitnesses,label="Average Fitness")
        plt.plot(self.min_fitnesses,label="Min Fitness")

        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.show()


    def take_population_snapshot(self,population):
      snapshot = population.getInformationOnPopulation()
      self.max_fitnesses.append(snapshot[0].fitness)
      self.average_fitnesses.append(snapshot[1].fitness)
      self.min_fitnesses.append(snapshot[2])