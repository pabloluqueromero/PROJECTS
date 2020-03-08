
from heapq import heappush, heappop,heapify
from search_space_methods import *
from itertools import count
from collections import deque
import numpy as np

def equivalent_configuration(position,size,configuration,component,equivalent):
	if position not in component:
		component.add(position)
		row,col = position//size,position%size
		if (row-1) >= 0:
			if position-size not in configuration: #UP
				equivalent_configuration(position-size,size,configuration,component,equivalent)
			else:
				equivalent.add(position-size)
		if (row+1) < size:
			if position+size not in configuration : #DOWN
				equivalent_configuration(position+size,size,configuration,component,equivalent)
			else:
				equivalent.add(position+size)

		if (col+1) < size:
			if position+1 not in configuration:#RIGHT
				equivalent_configuration(position+1,size,configuration,component,equivalent)
			else:
				equivalent.add(position+1)

		if (col-1) >= 0:
			if position-1 not in configuration: #LEFT
				equivalent_configuration(position-1,size,configuration,component,equivalent)
			else:
				equivalent.add(position-1)

def memoize(equivalent = False):
	cache = dict()
	cache_equivalent=dict()
	def decorator(f):
		def g(*args):
			if args not in cache:
				cache[args] = f(*args)
			return cache[args]
		def k(*args):
			size=args[0].size
			configuration =args[1]
			if configuration not in cache_equivalent:
				if len(configuration)/(size**2) < 0.3: #Wall percentage to try and avoid configuration whose equivalent is the same
					cache_equivalent[configuration] = configuration
				else:
					equivalent= set()
					equivalent_configuration(0,size,configuration,set(),equivalent)
					cache_equivalent[configuration] = frozenset(equivalent)
			if cache_equivalent[configuration] not in cache:
				cache[cache_equivalent[configuration]] = f(*args)
			return cache[cache_equivalent[configuration]]
		if equivalent:
			return k
		return g
	return decorator

def getProblemInstance(n,state):
	maze = np.zeros([n,n])
	for wall in state:
		i,j=wall//n,wall%n
		maze[i][j]=-1
	maze[0][0] = 1
	maze[0][(n-1)] = 2
	return maze

def A_StarImproved(walls,size,h,numberWalls=None):
	maxNumberNodes=0
	openNodes=[]
	heapify(openNodes)
	unique=count()
	heappush(openNodes,(0,next(unique),createNode2(size)))
	exploredStates=set()
	nodesGenerated=1
	expandedNodes=0
	while openNodes:
		maxNumberNodes = max(len(openNodes),maxNumberNodes)
		node=heappop(openNodes)[2]
		state=node[0]
		equivalentState= tuple(sorted(state))
		if equivalentState not in exploredStates:
			if testGoal2(node,size):
				return expandedNodes,node[2]
			expandedNodes+=1
			for succesor in expandNode2(walls,size,node):
				heappush(openNodes,(succesor[2]+h(size,succesor[0],numberWalls),next(unique),succesor)) 
				nodesGenerated+=1
			exploredStates.add(equivalentState)
	return expandedNodes ,-1

def printMaze(maze):
	for i in range(len(maze)):
		print('   | ',end='')
		for j in range(len(maze)):
			if maze[i][j] == -1:
				print(('{:^3}').format('■'),end='')
			elif maze[i][j] == 0:
				print('{:^3}'.format('·'),end='')
			else:
				print('{:^3}'.format(int(maze[i][j])),end='')
			if j<len(maze)-1:
				print(' ',end='')
		print('|')
	print('\n')

def heuristic2(size,state,numberWalls):
	total=0
	for car in state:
		total += (size-1) - (car//size)
		if car in numberWalls:
			total+=numberWalls[car]
	return total

def getWallsBeneathPositions(walls,size):
	numberWalls=dict()
	for wall in walls:
		column = wall % size
		row = wall // size
		for j in range(0,row):
			position = j*size+column
			if position not in walls:
				numberWalls[position]=1
			
	for pos in numberWalls:
		column = pos%size
		if column == 0 and ((pos + 1) in walls or (pos + 1)  in numberWalls):
			numberWalls[pos]+=1
		elif column == (size-1) and ((pos - 1) in walls or (pos - 1)  in numberWalls):
			numberWalls[pos]+=1
		elif ((pos - 1) in walls or (pos - 1)  in numberWalls) and ((pos + 1) in walls or (pos +1)  in numberWalls):
			numberWalls[pos]+=1

	return numberWalls

def get_max_mean(population):
	mean = 0
	best = -1
	for individual in population:
		best = max(best,individual[1][0])
		mean+=individual[1][0]
	return best,mean/len(population)
