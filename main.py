import tester

#Programmeinstiegspunkt
if __name__ == '__main__':
    print("Halloo")


    tester=tester.Tester()

    hyperparameters={"mutation_rate":0.2,"survivor_rate":0.1,"tournament_size":2}
    tester.createGAMaze(25,"RANDOM",100,"IMPROVED",hyperparameters,200)

    while True:
        pass



