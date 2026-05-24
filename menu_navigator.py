import tester
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
        self.tester = tester.Tester()

    def run_current_state(self):
        # Wir arbeiten direkt mit self.current_state, um die Kopier-Falle zu umgehen
        while self.current_state != self.END_STATE:

            # Bildschirm vor jedem neuen Zustand leeren für einen cleanen Look
            os.system('cls' if os.name == 'nt' else 'clear')

            if self.current_state == self.MAIN_MENU_STATE:
                self.main_menu()
            elif self.current_state == self.MAZE_GENERATOR_STATE:
                self.generator_menu()
            # TIPP: Hier kannst du später weitere Menüs einbauen

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
            print("\n[INFO] Starte Random Generation...")
            input("\nDrücke ENTER um fortzufahren...")
            # Wir bleiben im MAZE_GENERATOR_STATE, damit das Menü offen bleibt
            self.current_state = self.MAZE_GENERATOR_STATE

        elif selection == "EXECUTE_DFS":
            print("\n[INFO] Starte DFS Generation...")
            # self.tester.test_dfs_generation() # falls vorhanden
            input("\nDrücke ENTER um fortzufahren...")
            self.current_state = self.MAZE_GENERATOR_STATE

        elif selection == "EXECUTE_GA":
            print("\n[INFO] Starte GA Generation...")
            input("\nDrücke ENTER um fortzufahren...")
            self.current_state = self.MAZE_GENERATOR_STATE

        else:
            # Falls 'b' oder 'q' gewählt wurde, weisen wir den Zustand direkt zu
            self.current_state = selection