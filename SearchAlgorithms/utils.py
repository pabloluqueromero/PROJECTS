import random
def getProblemInstance(n, nCars, seed):
	maze = [[0 for i in range(n)] for j in range(n)]
	random.seed(seed)
	# number of walls
	nWalls = int(n * (n-2) * 0.2)
	# placing walls
	for _ in range(nWalls):
		maze[random.randint(0,n-3) + 1][random.randint(0,n-1)] = -1
		# placing cars, labelled as 1, 2, ..., nCars
	if (nCars > n):
		print('** Error **, number of cars must be <= dimension of maze!!')
		exit()
	l = [i for i in range(n)]
	for c in range(nCars):
		idx = random.randint(0,len(l)-1)
		maze[0][l[idx]] = c+1
		l.pop(idx)
	return maze


def printMaze(maze):
	for i in range(len(maze)):
		print('\t| ',end='')
		for j in range(len(maze)):
			if maze[i][j] == -1:
				print(('{:^3}').format('■'),end='')
			elif maze[i][j] == 0:
				print('{:^3}'.format('·'),end='')
			else:
				print('{:^3}'.format(maze[i][j]),end='')
			if j<len(maze)-1:
				print(' ',end='')
		print('|')
	print('\n')

# The method finalPositon is to move the cars form their initial position to their final position so that they can be printed later.

def finalPosition(state,maze):
	for car,i in zip(state,range(len(state))):
			maze[car//len(maze)][car%len(maze)]=i+1
	for i in range(len(maze)):
		maze[0][i]=0
	return maze
#
# Method to translate the solution provided by the algorithm
#
def translate(solution):
	solution.reverse()
	translated=[]
	for action in solution:
		if(action[0] == -1):
			translated.append('Car '+ str(action[1]+1) +' - LEFT')
		elif(action[0] == 1):
			translated.append('Car '+ str(action[1]+1) +' - RIGHT')
		elif(action[0]<0):
			translated.append('Car '+ str(action[1]+1) +' - UP')
		else:
			translated.append('Car '+ str(action[1]+1) +' - DOWN')
	return translated

