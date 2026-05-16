import matplotlib.pyplot as plt

import maze_renderer
import path_finder


class PopulationAnalyzer:

    def __init__(self):
        self.generation_data_packages=[]
        self.max_fitnesses = []
        self.average_fitnesses = []
        self.min_fitnesses = []
        self.unique_ratios =[]

    def update(self,data):
        self.generation_data_packages.append(data)

        self.max_fitnesses.append(data.max_fitness)
        self.average_fitnesses.append(data.average_fitness)
        self.min_fitnesses.append(data.min_fitness)
        self.unique_ratios.append(data.unique_ratio)

    def get_fittest_maze(self):
        return self.generation_data_packages[len(self.generation_data_packages)-1].fittest_maze


    def plot_fitness_convergence(self):

        plt.plot(self.max_fitnesses,label="Max Fitness")
        plt.plot(self.average_fitnesses,label="Average Fitness")
        plt.plot(self.min_fitnesses,label="Min Fitness")

        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.show()

    def plot_diversity(self):
        plt.plot(self.unique_ratios,label="Diversity")

        plt.xlabel("Generation")
        plt.ylabel("Diversity")

        plt.show()

    def render_fittest(self):
        path = path_finder.PathFinder().generatePath(self.get_fittest_maze())
        maze_renderer.MazeRenderer().renderPathInMaze(self.get_fittest_maze(), path)
