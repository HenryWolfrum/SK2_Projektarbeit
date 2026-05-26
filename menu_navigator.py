import menu_controller as m_c
import os
import sys
import maze_generator as m_g


class MenuNavigator:
    MAIN_MENU_STATE = "MAIN_MENU"
    MAZE_GENERATOR_STATE = "MAZE_GENERATION"
    AGENT_ENVIRONMENT_STATE = "AGENT_ENVIRONMENT"
    POPULATION_CREATOR_STATE = "POPULATION_CREATOR"
    TUNING_ANALYSIS_STATE = "TUNING_ANALYSIS"
    LOAD_STATE = "LOAD"
    END_STATE = "END_STATE"

    def __init__(self, start_state):
        self.current_state = start_state
        self.m_c = m_c.MenuController()

    def run_current_state(self):
        # Wir arbeiten direkt mit self.current_state, um die Kopier-Falle zu umgehen
        while self.current_state != self.END_STATE:

            # Bildschirm vor jedem neuen Zustand leeren für einen cleanen Look
            os.system('cls' if os.name == 'nt' else 'clear')

            if self.current_state == self.MAIN_MENU_STATE:
                self.main_menu()
            elif self.current_state == self.MAZE_GENERATOR_STATE:
                self.generator_menu()
            elif self.current_state == self.POPULATION_CREATOR_STATE:
                self.population_menu()
            elif self.current_state == self.TUNING_ANALYSIS_STATE:
                self.tuning_analysis_menu()
            elif self.current_state == self.AGENT_ENVIRONMENT_STATE:
                self.agent_env_menu()
            elif self.current_state == self.LOAD_STATE:
                self.loading_menu()

            else:
                print(f"\n[FEHLER] Illegaler Menü Zustand: {self.current_state}")
                print("-- Programm Abbruch ---")
                sys.exit(1)  # Beendet das Programm sauber mit Fehlercode

        # Regulärer Programm-Abbruch nach Schleifenende
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=========================================")
        print(" Programm wurde erfolgreich beendet!")
        print("=========================================")

    def main_menu(self):
        print("\n" + "=" * 50)
        print("      EVOLUTIONÄRE LABYRINTH GENERIERUNG        ")
        print("=" * 50)
        print(" [1] Labyrinth Generierung")
        print(" [2] Agent-Labyrinth Environment simulieren")
        print(" [3] Population erstellen und analysieren")
        print(" [4] Hyperparameter-Tuning & Algorithmen-Vergleichsanalyse")
        print(" [5] Labyrinth aus Speicher laden")
        print("")
        print(" [Q] Programm beenden (quit)")
        print("=" * 50)

        value_state_dict = {
            "1": self.MAZE_GENERATOR_STATE,
            "2": self.AGENT_ENVIRONMENT_STATE,
            "3": self.POPULATION_CREATOR_STATE,
            "4": self.TUNING_ANALYSIS_STATE,
            "5": self.LOAD_STATE,
            "q": self.END_STATE
        }

        query = input("▸ Aktionsbereich auswählen: ").strip().lower()
        while query not in value_state_dict:
            query = input("▸ Aktionsbereich auswählen: ").strip().lower()

        self.current_state = value_state_dict[query]

    def generator_menu(self):
        print("\n" + "=" * 50)
        print("      Labyrinth Generierung und Visualisierung       ")
        print("=" * 50)
        # Sehr gut gelöst!
        print(" [1] Labyrinth Typ: " + m_g.MazeGenerator().MODE_RANDOM)
        print(" [2] Labyrinth Typ: " + m_g.MazeGenerator().MODE_RANDOM_DFS)
        print(" [3] Labyrinth Typ: " + m_g.MazeGenerator().MODE_GENETIC_ALGORITHM)
        print("")
        print(" [B] Zurück zum Hauptmenü (back)")
        print(" [Q] Programm beenden (quit)")
        print("=" * 50)

        value_state_dict = {
            "1": "EXECUTE_RANDOM",
            "2": "EXECUTE_DFS",
            "3": "EXECUTE_GA",
            "b": self.MAIN_MENU_STATE,
            "q": self.END_STATE
        }

        query = input("▸ Generierungsart auswählen: ").strip().lower()
        while query not in value_state_dict:
            query = input("▸ Generierungsart auswählen: ").strip().lower()

        selection = value_state_dict[query]

        if selection == "EXECUTE_RANDOM":
            print("\n[INFO] Starte Random Generierung...")
            self.m_c.createRandomMaze()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")

            # Wir bleiben im MAZE_GENERATOR_STATE, damit das Menü offen bleibt
            self.current_state = self.MAZE_GENERATOR_STATE

        elif selection == "EXECUTE_DFS":
            print("\n[INFO] Starte DFS Generierung...")
            self.m_c.createRandomDFSMaze()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")

            self.current_state = self.MAZE_GENERATOR_STATE

        elif selection == "EXECUTE_GA":
            print("\n[INFO] Starte GA Generierung...")
            self.m_c.createGAMaze()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")

            self.current_state = self.MAZE_GENERATOR_STATE

        else:
            # Falls 'b' oder 'q' gewählt wurde, weisen wir den Zustand direkt zu
            self.current_state = selection



    def agent_env_menu(self):
        print("\n" + "=" * 50)
        print("      Agenten Simulations Spiel       ")
        print("=" * 50)

        print(" [1] Greedy Agenten auf Maze spielen")
        print("")
        print(" [B] Zurück zum Hauptmenü (back)")
        print(" [Q] Programm beenden (quit)")
        print("=" * 50)

        value_state_dict = {
            "1": "EXECUTE_GAME",
            "b": self.MAIN_MENU_STATE,
            "q": self.END_STATE
        }

        query = input("▸ Simulationsaktion wählen: ").strip().lower()
        while query not in value_state_dict:
            query = input("▸ Simulationsaktion wählen: ").strip().lower()

        selection = value_state_dict[query]

        if selection == "EXECUTE_GAME":
            self.m_c.agent_game()

        else:
            self.current_state = selection



    def population_menu(self):
        print("\n" + "=" * 50)
        print("      Population Simulationsumgebung       ")
        print("=" * 50)

        print(" [1] Population simulieren und auswerten")
        print("")
        print(" [B] Zurück zum Hauptmenü (back)")
        print(" [Q] Programm beenden (quit)")
        print("=" * 50)

        value_state_dict = {
            "1": "EXECUTE_POPULATION",
            "b": self.MAIN_MENU_STATE,
            "q": self.END_STATE
        }

        query = input("▸ Populationsaktion wählen: ").strip().lower()
        while query not in value_state_dict:
            query = input("▸ Populationsaktion wählen: ").strip().lower()

        selection = value_state_dict[query]

        if selection == "EXECUTE_POPULATION":
            print("\n[INFO] Starte Populationsumgebung...")
            self.m_c.createPopulation()
            print("\n[INFO] Drücke ENTER um zurückzukehren...")
        else:
            self.current_state = selection

    def loading_menu(self):
        print("\n" + "=" * 50)
        print("      Labyrinth-Speicher       ")
        print("=" * 50)
        print(" [1] Labyrinth mit Namen laden")
        print(" [2] Gespeicherte Namen anzeigen")
        print(" [3] Labyrinth mit Namen löschen: " )
        print("")
        print(" [B] Zurück zum Hauptmenü (back)")
        print(" [Q] Programm beenden (quit)")
        print("=" * 50)

        value_state_dict = {
            "1": "EXECUTE_LOAD",
            "2": "EXECUTE_LIST",
            "3": "EXECUTE_DELETE",
            "b": self.MAIN_MENU_STATE,
            "q": self.END_STATE
        }

        query = input("▸ Speicheroperation auswählen: ").strip().lower()
        while query not in value_state_dict:
            query = input("▸ Speicheroperation auswählen: ").strip().lower()

        selection = value_state_dict[query]

        if selection == "EXECUTE_LOAD":
            print("\n[INFO] Starte Ladevorgang...")
            self.m_c.load_maze()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")
            self.current_state = self.LOAD_STATE
        elif selection == "EXECUTE_LIST":
            print("\n[INFO] Starte Speicherauswertung...")
            self.m_c.list_maze_storage()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")
            self.current_state = self.LOAD_STATE
        elif selection == "EXECUTE_DELETE":
            self.m_c.delete_maze()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")
            self.current_state = self.LOAD_STATE
        else:
            self.current_state = selection

    def tuning_analysis_menu(self):
        print("\n" + "=" * 50)
        print("      Tuning und Analyseumgebung       ")
        print("=" * 50)

        print(" [1] Algorithmen vergleichen")
        print(" [2] Hyperparameteroptimierung Ergebnisse laden ")
        print(" [3] Hyperparameteroptimierung durchführen")

        print("")
        print(" [B] Zurück zum Hauptmenü (back)")
        print(" [Q] Programm beenden (quit)")
        print("=" * 50)

        value_state_dict = {
            "1": "EXECUTE_COMPARSION",
            "2": "EXECUTE_TUNING_PLOTTING",
            "3": "EXECUTE_TUNING",
            "b": self.MAIN_MENU_STATE,
            "q": self.END_STATE
        }

        query = input("▸ Analysefunktion auswählen: ").strip().lower()
        while query not in value_state_dict:
            query = input("▸ Analysefunktion auswählen: ").strip().lower()

        selection = value_state_dict[query]

        if selection == "EXECUTE_COMPARSION":
            self.m_c.compare_algorithms()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")
            self.current_state = self.TUNING_ANALYSIS_STATE
        elif selection == "EXECUTE_TUNING_PLOTTING":
            self.m_c.plot_tuning_results()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")
            self.current_state = self.TUNING_ANALYSIS_STATE
        elif selection == "EXECUTE_TUNING":
            self.m_c.hyperparameter_tuning()
            input("\n[INFO] Drücke ENTER um zurückzukehren ...")
            self.current_state = self.TUNING_ANALYSIS_STATE

        else:
            self.current_state = selection