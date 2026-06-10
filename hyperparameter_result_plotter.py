
import json
import matplotlib.pyplot as plt


def plot_tuning_results(show_std=False):
    # JSON-Datei laden
    with open("hyperparameter_tuning_results.json") as f:
        data = json.load(f)

    # Alle Hyperparameter sammeln
    mutation_rates = sorted(set(d["mutation_rate"] for d in data))
    survivor_rates = sorted(set(d["survivor_rate"] for d in data),reverse=True)
    tournament_sizes = sorted(set(d["tournament_size"] for d in data))

    # Lookup für Fitness-Werte
    lookup = {(d["mutation_rate"],d["survivor_rate"],d["tournament_size"]): d["fitness"]for d in data}

    # Lookup für Standardabweichung
    std_lookup = {(d["mutation_rate"],d["survivor_rate"],d["tournament_size"]): d["standard_deviation"]for d in data}

    # Min/Max für Farbskala
    fitness_vals = list(lookup.values())
    vmin = min(fitness_vals)
    vmax = max(fitness_vals)
    mid = (vmin + vmax) / 2

    # Figure mit 2x2 Subplots erzeugen (falls 4 verschiedene Tournament Größen gewählt wurden)
    fig, axes = plt.subplots(2,2,figsize=(14, 10),sharex=True,sharey=True,constrained_layout=True)

    # Für jede Tournament Size eine Heatmap zeichnen
    for ax, t_size in zip(axes.flat, tournament_sizes):

        # Matrix für Heatmap erzeugen
        grid = [[lookup.get((m, s, t_size), 0.0)for m in mutation_rates]for s in survivor_rates]

        # Heatmap zeichnen
        im = ax.imshow(grid,cmap="viridis",vmin=vmin,vmax=vmax,aspect="auto")

        # Zahlen in die Heatmap schreiben
        for y, row in enumerate(grid):
            for x, val in enumerate(row):

                text_color = ("white" if val < mid else "black")

                # Fitness-Wert
                ax.text(x,y - 0.12 if show_std else y,f"{val:.3f}",ha="center",va="center",fontsize=9,fontweight="bold",color=text_color)

                # ggf. Standardabweichung anzeigen
                if show_std:

                    std_val = std_lookup.get((mutation_rates[x],survivor_rates[y],t_size),0.0)

                    ax.text(x,y + 0.18,f"±{std_val:.3f}",ha="center",va="center",fontsize=7,color=text_color)

        # Titel des Subplots
        ax.set_title(f"Tournament Size: {t_size}",fontsize=12,fontweight="bold")

        # X-Achse
        ax.set_xticks(range(len(mutation_rates)))
        ax.set_xticklabels([f"{m:.0%}" for m in mutation_rates])

        # Y-Achse
        ax.set_yticks(range(len(survivor_rates)))
        ax.set_yticklabels([f"{s:.0%}" for s in survivor_rates])

        # Achsen hier beschriften
        ax.tick_params(labelbottom=True)

        ax.set_xlabel("Mutation Rate")
        ax.set_ylabel("Survivor Rate")

    # Nicht verwendete Subplots ausblenden
    for ax in axes.flat[len(tournament_sizes):]:
        ax.set_visible(False)

    # Farbskala hinzufügen am Rand
    fig.colorbar(im,ax=axes.ravel().tolist(),shrink=0.6,label="Fitness"
    )

    # Titel anzeigen
    fig.suptitle("GA Hyperparameter Tuning Results",fontsize=16,fontweight="bold")

    # Plot anzeigen
    plt.show()




