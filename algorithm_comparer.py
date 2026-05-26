from maze_generator import MazeGenerator as mg
import fitness_evaluator
import matplotlib.pyplot as plt


def _evaluate_worker_batch(run, algorithm, batch_size, compare_function):
    generator = mg()
    fe = fitness_evaluator.FitnessEvaluator()

    results = []

    if algorithm[0] == "G":
        for _ in range(batch_size):
            maze_obj = generator.geneticAlgorithmMaze(
                25,
                "RANDOM",
                algorithm[1],
                compare_function,
                algorithm[2],
                algorithm[3]
            )
            # Generator kann None zurückgeben (z.B. kein Pfad gefunden)
            if maze_obj is None:
                continue
            results.append(fe.calcFitness(maze_obj, compare_function))

    else:
        mode_map = {"R": mg.MODE_RANDOM, "D": mg.MODE_RANDOM_DFS}
        mode = mode_map[algorithm[0]]
        for _ in range(batch_size):
            maze_obj = generator.generateMaze(25, mode)
            if maze_obj is None:
                continue
            results.append(fe.calcFitness(maze_obj, compare_function))


    return {"algorithm": algorithm, "run": run, "fitness": max(results, default=0)}


class AlgorithmComparer:

    DEFAULT_COMPARE_SET = [
        mg.MODE_RANDOM,
        mg.MODE_RANDOM_DFS,
        mg.MODE_GENETIC_ALGORITHM
    ]
    DEFAULT_COMPARE_FUNCTION = fitness_evaluator.FitnessEvaluator().FUNCTION_IMPROVED
    DEFAULT_EXPERIMENT_RUNS = 30

    def __init__(self, compare_set=None, compare_function=None):

        if not compare_set:
            compare_set = self.DEFAULT_COMPARE_SET

        max_budget = 1
        for algo in compare_set:
            if algo[0] == "G":
                evals = algo[4]
                if evals > max_budget:
                    max_budget = evals

        self.evaluation_budget = max_budget
        self.compare_set = compare_set
        self.compare_function = compare_function or self.DEFAULT_COMPARE_FUNCTION

    def _algo_label(self, algo):
        if algo[0] == "R":
            return "RANDOM"
        if algo[0] == "D":
            return "RANDOM_DFS"
        hp = algo[2]
        return (
            f"GENETIC_ALGORITHM\n"
            f"pop={algo[1]}  gen={algo[3]}\n"
            f"mut={hp['mutation_rate']}  "
            f"surv={hp['survivor_rate']}  "
            f"tour={hp['tournament_size']}"
        )

    def build_tasks(self, experiment_runs=DEFAULT_EXPERIMENT_RUNS):
        tasks = []
        for algorithm in self.compare_set:

            cost = int(algorithm[len(algorithm) - 1])
            batch_size = self.evaluation_budget // cost
            for run in range(experiment_runs):
                tasks.append((run, algorithm, batch_size, self.compare_function))
        return tasks

    def aggregate_results(self, raw_results):
        # Use string labels as keys instead of raw tuples (tuples with dicts are unhashable)
        compare_data = {self._algo_label(alg): [] for alg in self.compare_set}
        for res in raw_results:
            compare_data[self._algo_label(res["algorithm"])].append(res["fitness"])
        return compare_data

    def plot_results(self, compare_data):
        labels = list(compare_data.keys())  # already strings
        plt.boxplot(list(compare_data.values()), tick_labels=labels)
        plt.ylabel("Fitness")
        plt.xlabel("Algorithmus")
        plt.title("Algorithmenvergleich")
        plt.show()