from functools import partial
'''
  State= a tuple of size n where position i == j means: car number (i+1) is in position j of the maze
 
 			To reverse the encoding and extract the row and the column of a car we proceed as follows:
 			row= encodedPosition // len(maze)
 			column= encodedPosition % len(maze)
 
  Example : state= (20,10,6,5) 
 						-> Car 1 in position 20 
 						-> Car 2 in position 10
 						-> Car 3 in position 6
 						-> Car 4 in position 5

  In this case we represent a node as a tuple : (State, parent, cost , action ,depth)
  It is slighty heavier than using the class Node, however we have found that we get much better results timewise.
  Specially when it comes to heavier computations we get up to 60 sec improvements. This happens because of
  internal memory storage in continuous memory address, making the access quicker and more efficient.

'''
def createNode2(size):
	initialState=(0,size-1)
	return (initialState,None,0,None,0)		
'''
  We use a generator so that as soon as a car is not found in the last row, we return false
  In most cases, we don't need to check all the cars, we are able to give an answer before reaching the end, if it is the case.
'''
def testGoal2(node,n):
	return all(((car // n) == (n-1)) for car in node[0])

'''
 	We use a map function to return an iterator that will save space, so that we don't have simultaneously
 	a list of successors and the list of open nodes. 
 
 	METHOD EXPLANATION:
 	For every action in  possibleActions we generate a node using applyAction
 	We use partial to dynamically generate a new method that only takes one argument
 	It is cheaper to do this than creating a lambda function that will add an overhead.
'''

def expandNode2(walls,size,node):
	return map(partial(applyAction2,node),possibleActions(walls,size,node[0]))

'''
 	METHOD EXPLANATION:
 	We have nodes linked to their parents so we walk up the path until we reach the root -- Initial Node
'''

def recoverPath2(node):
	path=[]
	while node[1]:
		path.append(node[3])   # [(Action,Car)]  Action -> { -size , size , 1 , -1 }
		node=node[1]
	return path
	
'''
 	METHOD EXPLANATION:
 	For every car in the state we check the following 3 conditions for the 4 movements:
 		1.Out of bounds
 		2.We check if there is a wall
 		3.We check if another car is already in that position
 		
 		Actions are encoded as follow : (UP == -size), (DOWN == +size), (LEFT == -1), (RIGHT == +1) 
 		possibleActions returns a list of tuples (action,car) size 4*N , N == len(state), in the worst case.
'''
def possibleActions(walls,size,state):
	actions=[]
	for index,carPosition in enumerate(state):
		current_row=carPosition//size
		current_col= carPosition%size

 		 #UP
		new_row=current_row-1
		next_state= new_row*size + current_col
		if new_row >= 0 and next_state not in walls and next_state not in state :
			actions.append([size*(-1),index])
		
		 #RIGHT
		new_col=current_col+1
		next_state = current_row*size + new_col
		if (new_col) < size and next_state not in walls and next_state not in state:
			actions.append([1,index])
			
		 #LEFT
		new_col=current_col-1
		next_state=current_row*size + new_col
		if  (new_col) >= 0 and next_state not in walls and next_state not in state:
			actions.append([-1,index])
			
		 #DOWN
		new_row=current_row+1
		next_state=new_row*size + current_col
		if (new_row) < size and next_state not in walls and next_state not in state:
			actions.append([size,index])

	return actions
'''
 In this case I have made applyAction generate not only a new state but the new node. 
 It saves having to write more code in expand node.
 
 	METHOD EXPLANATION:
 	As a state is a represented by a tuple I need to create a list that I will later on turn into a tuple:
 		-action is a tuple containing = ( action , car )
 		1.Rewrite the state but applying the action -> (action[0]) to car in index-> (action[1]).
 		2.Cast the state as a tuple and create a NewNode with that state and with the information of the parent node.
'''
	
def applyAction2(node,action):
	newState=tuple([node[0][i]+action[0] if i == action[1] else _ for i, _ in enumerate(node[0])])
	return (newState,node,node[2]+1,action,node[4]+1)

