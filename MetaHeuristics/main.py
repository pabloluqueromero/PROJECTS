from GeneticAlgorithm import GeneticAlgorithm
from HillClimbing import HillClimbing
from time import time
from sys import argv
from utils import printMaze,getProblemInstance


'''
main.py 10 219 -- HillClimbing 1 1 empty ILS
main.py 8 219 -- Genetic 200 10 1 truncation 0.95 0.1 rank
'''


if len(argv)< 5:
    print("Wrong number of parameters: size seed -- algorithm ...options...")
    exit()
algorithm = argv[4]


if algorithm =="HillClimbing":  
    if len(argv)< 9:
        print("Wrong number of parameters: size seed -- HillClimbing numberIterations distance {empty/random} {ILS/RLS} {number_perturbation_for_ILS}")
        exit()
    # Parsing input
    datatype = [int,int,str,str,int,int,str,str]
    size,seed,_,_,num_iterations,distance,empty,option=map(lambda x: x[0](x[1]) ,zip(datatype,argv[1:]))
    perturbations=1
    if option == "ILS":
        if len(argv)>9:
            perturbations = int(argv[9])

    #Initialising object
    hc = HillClimbing(size,seed,num_iterations,distance,perturbations,empty == "empty")

    startTime = time()
    sol,total_number_individuals = None,0
    if option == "ILS":
        sol,total_number_individuals = hc.ILS()
    elif option == "RLS":
        sol,total_number_individuals = hc.RLS()
    else:
        print("Unknow Algorithm")
        exit()
    elapsed_time = time()-startTime

    #Printing output
    print("\n------------ SOLUTION ------------\n")
    printMaze(getProblemInstance(size,sol[0]))
    print("------------- OUTPUT -------------\n")
    print("Solution : {}\nExpanded Nodes: {}\nCost of the solution: {}\nElpased Time: {}\n".format(list(sol[0]),sol[1][0],sol[1][1],elapsed_time))

    print("\nAlgorithm: {}".format(option))
    if option == "ILS":
        print("Number of perturbations: {}".format(min(size**2-size - size,perturbations)))
    print("Individuals evaluated: {}".format(total_number_individuals))
    print("-----------------------------------\n") 
    exit()


else:
    if len(argv)<11:
        print("Wrong number of parameters: size seed -- GeneticAlgorithm individuals generations number_points {elitism/truncation} crossover_probability mutation_probability {Rank}")
        exit()

    #Parsing input
    input_type = [int,int,str,str,int,int,int,str,float,float]
    if len(argv)>10:
        selection="rank"
    else:
        selection = ""
    size,seed,_,_,individuals,generations,number_points,combine,crossover_probability,mutation_probability = map(lambda x : x[0](x[1]),zip(input_type,argv[1:]))

    #Initilialising object
    ga = GeneticAlgorithm(size,seed,individuals,generations,number_points,crossover_probability,mutation_probability,selection,combine)

    #Executing algorithm
    startTime = time()
    sol = max(ga.execute_algorithm(),key = lambda x : x[1][0])
    elapsed_time =time()-startTime
    print("\n------------ SOLUTION ------------\n")
    printMaze(getProblemInstance(size,sol[0]))
    print("------------- OUTPUT -------------\n")
    print("Solution : {}\nExpanded Nodes: {}\nCost of the solution: {}\nElpased Time: {}\n".format(list(sol[0]),sol[1][0],sol[1][1],elapsed_time))
    print("-----------------------------------\n")
    exit()