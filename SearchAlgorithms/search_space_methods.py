from node import Node
# State= a tuple of size n where position i == j means: car number (i+1) is in position j of the maze
#
#			To reverse the encoding and extract the row and the column of a car we proceed as follows:
#			row= encodedPosition // len(maze)
#			column= encodedPosition % len(maze)
#
# Example : state= (20,10,6,5) 
#						-> Car 1 in position 20 
#						-> Car 2 in position 10
#						-> Car 3 in position 6
#						-> Car 4 in position 5


#	OBTAINING THE INITIAL STATE:
#
#	1.What we do here is first assign to each car, their position with enumerate. 
#	2.Then we keep only the cars removing the elements that are free cells, with filter.
#	3.Then we sort it by the second element, we obtain something like :(posCar1,car1),(posCar2,car2),(posCar3,car3)...
#	4.We have the cars in order indicating their position. i.e. (3,1),(5,2) -> Car 1 is in position 3, car 2 is in position 5 -> state= (3,5)
#	5.We take the first element, putting only the position of each car in the state.

def create_node(maze):
	initialState=tuple([x for x,_ in sorted(filter(lambda x: x[1] != 0, enumerate(maze[0])),key= lambda x: x[1])])
	return Node(initialState)


# We use a generator so that as soon as a car is not found in the last row, we return false
# In most cases, we don't need to check all the cars, we are able to give an answer before reaching the end, if it is the case.
def test_goal(node,n):
	return all(((car // n) == (n-1)) for car in node.state)



#	We use a map function to return an iterator that will save space, so that we don't have simultaneously
#	a list of successors and the list of open nodes. 
#
#	METHOD EXPLANATION:
#	For every action in  possibleActions we generate a node using apply_action
#	We use partial to dynamically generate a new method that only takes one argument
#	It is cheaper to do this than creating a lambda function that will add an overhead.

def expand_node(maze,node):
	return map(lambda action:apply_action(node,action),possibleActions(maze,node.state))


#	METHOD EXPLANATION:
#	We have nodes linked to their parents so we walk up the path until we reach the root -- Initial Node


def recover_path(node):
	path=[]
	while node.parent_node:
		path.append(node.action)   #[(Action,Car)]  Action -> { -size , size , 1 , -1 }
		node=node.parent_node
	return path
	

#	METHOD EXPLANATION:
#	For every car in the state we check the following 3 conditions for the 4 movements:
#		1.Out of bounds
#		2.We check if there is a wall
#		3.We check if another car is already in that position
#		
#		Actions are encoded as follow : (UP == -size), (DOWN == +size), (LEFT == -1), (RIGHT == +1) 
#		possibleActions returns a list of tuples (action,car) size 4*N , N == len(state), in the worst case.

def possibleActions(maze,state):
	actions=[]
	size=len(maze)
	for index,car_position in enumerate(state):
		current_row=car_position//size
		current_col= car_position%size

 		#UP
		new_row=current_row-1
		if new_row >= 0 and maze[new_row][current_col] != -1 and (new_row*size + current_col) not in state:
			actions.append([size*(-1),index])
		
		#RIGHT
		new_col=current_col+1
		if (new_col) < size and maze[current_row][new_col] != -1 and (current_row*size + new_col) not in state:
			actions.append([1,index])
			
		#LEFT
		new_col=current_col-1
		if  (new_col) >= 0 and maze[current_row][new_col] != -1 and (current_row*size + new_col) not in state:
			actions.append([-1,index])
			
		#DOWN
		new_row=current_row+1
		if (new_row) < size and maze[new_row][current_col] != -1 and (new_row*size + current_col) not in state:
			actions.append([size,index])

	return actions


#In this case I have made apply_action generate not only a new state but the new node. 
#It saves having to write more code in expand node.
#
#	METHOD EXPLANATION:
#	As a state is a represented by a tuple I need to create a list that I will later on turn into a tuple:
#		-action is a tuple containing = ( action , car )
#		1.Rewrite the state but applying the action -> (action[0]) to car in index-> (action[1]).
#		2.Cast the state as a tuple and create a NewNode with that state and with the information of the parent node.

def apply_action(node,action):
	new_state=tuple([node.state[i]+action[0] if i == action[1] else _ for i, _ in enumerate(node.state)])
	return Node(state=new_state,parent_node=node,action=action,depth=node.depth+1,path_cost=node.path_cost+1)


#############################################################################################################
#
#
#Same methods for a different codification of the node that doesn't use a Node class, instead they use a tuple.
#
#
#############################################################################################################


# In this case I represent a node as a tuple : (State, parent, cost , action ,depth)
# It is slighty heavier than using the class Node, however I have found that I get much better results timewise.
# Specially when it comes to heavier computations I get up to 60 sec improvements. This happens because of
# internal memory storage in continuous memory address, making the access quicker and more efficient.


# METHODS: All this methods work exactly as the ones above however the node is addressed in a different way.
# For any clarifications, please refer to the aforementioned methods with their corresponding explanation.


def create_node2(maze):
	initialState=tuple([x for x,_ in sorted(filter(lambda x: x[1] != 0, enumerate(maze[0])),key=lambda x : x[1])])
	return (initialState,None,0,None,0)		

def test_goal2(node,n):
	return all(((car // n) == (n-1)) for car in node[0])

def expand_node2(maze,node):
	return map(lambda action: apply_action2(node,action),possibleActions(maze,node[0]))
	
def apply_action2(node,action):
	new_state=tuple([node[0][i]+action[0] if i == action[1] else _ for i, _ in enumerate(node[0])])
	return (new_state,node,node[2]+1,action,node[4]+1)

def recover_path2(node):
	path=[]
	while node[1]:
		path.append(node[3])   #[(Action,Car)]  Action -> { -size , size , 1 , -1 }
		node=node[1]
	return path


