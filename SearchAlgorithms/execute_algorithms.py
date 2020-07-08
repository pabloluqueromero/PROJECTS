from sys import argv,exit,getsizeof
import random
from search_algorithms import *
from search_space_methods import *
from time import time
from node import Node
from utils import *


# To execute the algorithmos run the following line:
# python3 execute_algorithms.py size numberOfCars seed -- AlgorithmName(Improved) limit/heuristic

algorithms = {
	'DepthFirstSearch': DepthFirstSearch,
	'BreadthFirstSearch': BreadthFirstSearch,
	'DepthLimitedSearch': DepthLimitedSearch,
	'IterativeDeepeningSearch': IterativeDeepeningSearch,
	'AStar':AStar,
	'BestFirst':BestFirst,

	
	'DepthFirstSearchImproved': DepthFirstSearchImproved,
	'BreadthFirstSearchImproved': BreadthFirstSearchImproved,
	'DepthLimitedSearchImproved': DepthLimitedSearchImproved,
	'IterativeDeepeningSearchImproved': IterativeDeepeningSearchImproved,
	'AStarImproved':AStarImproved,
	'BestFirstImproved':BestFirstImproved
}


if len(argv) < 6:
	print('Wrong number of parameters.')
	exit()
size=int(argv[1])
n_cars=int(argv[2])
seed= int(argv[3])
algorithm_name=argv[5]
maze=getProblemInstance(size,n_cars,seed)

output=None
factor=0

print('\n X = Wall')
print(' . = Free cell\n')
printMaze(maze)
print('---------------------------------------\n')


# I check what algorithm we are running and I set the size of a node to calculate memory usage later
if 'Improved' in argv[5]:
	factor=getsizeof(create_node2(maze))
else:
	factor=getsizeof(create_node(maze))

limit = int(argv[6]) if len(argv)==7 else float('inf')
heuristic = int(argv[6]) if len(argv)==7 else None

print(f'Executing {algorithm_name}')
start_time = time()
if "Limit" in algorithm_name:
	output=algorithms[algorithm_name](maze,limit = limit).perform_search()
elif "BestFirst" in algorithm_name or "AStar" in algorithm_name:
	output=algorithms[algorithm_name](maze,heuristic = heuristic).perform_search()
else:
	output=algorithms[algorithm_name](maze).perform_search()

totalTime=(time() - start_time)
if output!= None:
	if output[2] == None:
		nodesGenerated,maxN,sol,expandedNodes = output
		print('\n---------------------------------------\n')
		print('NO SOLUTION FOUND')
	
	else:
		nodesGenerated,maxN,state,expandedNodes,sol,cost = output
		print('\n---------------------------------------\n')
		print('Solution state: ', state,'\n')
		printMaze(finalPosition(state,maze))
		print('---------------------------------------\n')
		print('Solution lenght: ',len(sol))
		print('Solution cost: ', cost )

	print('Elapsed time:',totalTime,' seconds')
	print('\nGenerated nodes: ', nodesGenerated)
	print('Expanded nodes: ',expandedNodes)
	print('Maximum minimum number of nodes simultaneously in memory: ', maxN)
	print('Maximum minimum memory usage (by open nodes): ', maxN*factor* 2**(-20), 'MB')
	print('\n---------------------------------------\n')
	if output[2] != None:
		y=''
		while(y not in['yes','no']):
			print('Would you like to see the actions? (yes/no)')
			y=input()
		if(y == 'yes'):
			for i in translate(sol):
				print(i)
else:
	print('Unknown algorithm.\nMake sure you are using one of these (or their Improved version):')
	print('DepthFirstSearch - BreadthFirstSearch - DepthLimitedSearch - IterativeDeepeningSearch - BestFirst - AStar')
	exit()