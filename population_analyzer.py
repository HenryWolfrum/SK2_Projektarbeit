import matplotlib.pyplot as plt

class PopulationAnalyzer:

    def __init__(self):
        self.generation_data_packages=[]
        self.max_fitnesses = []
        self.average_fitnesses = []
        self.min_fitnesses = []
        self.unique_ratios =[]


    #Nimmt ein neues Datenpacket auf
    def update(self,data):
        self.generation_data_packages.append(data)

        self.max_fitnesses.append(data.max_fitness)
        self.average_fitnesses.append(data.average_fitness)
        self.min_fitnesses.append(data.min_fitness)
        self.unique_ratios.append(data.unique_ratio)

    #Gibt das fitteste Labyrinth zurück
    def get_fittest_maze(self):
        return self.generation_data_packages[len(self.generation_data_packages)-1].fittest_maze


    #Zeichnet die Fitnesskonvergenz basierend der gesammelten Daten
    def plot_fitness_convergence(self):

        plt.plot(self.max_fitnesses,label="Max Fitness")
        plt.plot(self.average_fitnesses,label="Average Fitness")
        plt.plot(self.min_fitnesses,label="Min Fitness")

        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.show()

    #Zeichnet die Diversität
    def plot_diversity(self):
        plt.plot(self.unique_ratios,label="Diversity")

        plt.xlabel("Generation")
        plt.ylabel("Diversity")

        plt.show()
