import json
import matplotlib.pyplot as plt

with open("hyperparameter_tuning_results.json") as f:
    data = json.load(f)

mutation_rates   = sorted(set(d["mutation_rate"]   for d in data))
survivor_rates   = sorted(set(d["survivor_rate"]   for d in data), reverse=True)
tournament_sizes = sorted(set(d["tournament_size"] for d in data))

lookup = {(d["mutation_rate"], d["survivor_rate"], d["tournament_size"]): d["fitness"]
          for d in data}

fitness_vals = list(lookup.values())
vmin, vmax = min(fitness_vals), max(fitness_vals)
mid = (vmin + vmax) / 2

fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True,
                         constrained_layout=True)

for ax, t_size in zip(axes.flat, tournament_sizes):
    grid = [
        [lookup.get((m, s, t_size), 0.0) for m in mutation_rates]
        for s in survivor_rates
    ]

    im = ax.imshow(grid, cmap="viridis", vmin=vmin, vmax=vmax, aspect="auto")

    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            ax.text(x, y, f"{val:.3f}", ha="center", va="center", fontsize=9,
                    color="white" if val < mid else "black")

    ax.set_title(f"Tournament Size: {t_size}", fontsize=12, fontweight="bold")
    ax.set_xticks(range(len(mutation_rates)))
    ax.set_xticklabels([f"{m:.0%}" for m in mutation_rates])
    ax.set_yticks(range(len(survivor_rates)))
    ax.set_yticklabels([f"{s:.0%}" for s in survivor_rates])
    ax.tick_params(labelbottom=True)  # ← fix: Labels immer anzeigen
    ax.set_xlabel("Mutation Rate")
    ax.set_ylabel("Survivor Rate")

for ax in axes.flat[len(tournament_sizes):]:
    ax.set_visible(False)

fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6, label="Fitness")
fig.suptitle("GA Hyperparameter Tuning Results", fontsize=16, fontweight="bold")

plt.show()