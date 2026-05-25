from maze_generator import MazeGenerator as mg
import fitness_evaluator
import matplotlib.pyplot as plt

def _evaluate_worker_batch(run, algorithm, batch_size, maze_size, compare_function):
    generator = mg()
    fe = fitness_evaluator.FitnessEvaluator()

    results = [
        fe.calcFitness(generator.generateMaze(maze_size, algorithm), compare_function)
        for _ in range(batch_size)
    ]

    return {"algorithm": algorithm, "run": run, "fitness": max(results)}

class AlgorithmComparer:

    DEFAULT_COMPARE_SET = [mg.MODE_RANDOM, mg.MODE_RANDOM_DFS, mg.MODE_GENETIC_ALGORITHM]
    DEFAULT_COMPARE_FUNCTION = fitness_evaluator.FitnessEvaluator().FUNCTION_IMPROVED
    DEFAULT_EXPERIMENT_RUNS = 30

    # Kosten pro einzelnem Algorithmus-Aufruf
    EVALUATION_COSTS = {
            mg.MODE_RANDOM: 1,
            mg.MODE_RANDOM_DFS: 1,
            mg.MODE_GENETIC_ALGORITHM: None,  # wird aus generations * population_size berechnet
    }

    def __init__(self, generations, population_size, compare_set=None, compare_function=None):

            self.evaluation_budget = generations * population_size

            self.evaluation_costs = self.EVALUATION_COSTS.copy()
            self.evaluation_costs[mg.MODE_GENETIC_ALGORITHM] = self.evaluation_budget

            self.compare_set = compare_set or self.DEFAULT_COMPARE_SET.copy()
            self.compare_function = compare_function or self.DEFAULT_COMPARE_FUNCTION

    def build_tasks(self, experiment_runs=DEFAULT_EXPERIMENT_RUNS):
            tasks = []
            for algorithm in self.compare_set:
                cost = self.evaluation_costs[algorithm]
                batch_size = self.evaluation_budget // cost
                for run in range(experiment_runs):
                    tasks.append((run, algorithm, batch_size, self.compare_function))
            return tasks

    def aggregate_results(self, raw_results):
        compare_data = {alg: [] for alg in self.compare_set}
        for res in raw_results:
            compare_data[res["algorithm"]].append(res["fitness"])
        return compare_data

    def plot_results(self, compare_data):
        plt.boxplot(list(compare_data.values()), tick_labels=list(compare_data.keys()))
        plt.ylabel("Fitness")
        plt.xlabel("Algorithm")
        plt.title("Algorithm Comparison")
        plt.show()

