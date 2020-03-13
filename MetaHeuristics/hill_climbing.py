import random
from itertools import combinations
from utils import memoize,A_StarImproved,getWallsBeneathPositions,getProblemInstance,heuristic2,printMaze

class HillClimbing:
	
	@memoize(equivalent=False)
	def evaluate(self,state):
		self.not_repeated+=1
		return A_StarImproved(state,self.size,heuristic2,getWallsBeneathPositions(state,self.size))

	def generate_sample(self):
		possible_walls = range(self.size,(self.size**2)- self.size)
		random_size = random.randint(0,(self.size**2)-2*self.size)
		return frozenset(random.sample(possible_walls,random_size))

	def change_position(self,state,walls):
		neighbour = set(state)
		walls_to_remove = neighbour.intersection(walls)
		neighbour.update(walls)
		neighbour.difference_update(walls_to_remove)
		return frozenset(neighbour)

	def generate_neighbours(self,state):
		lower_bound = self.size
		upper_bound = (self.size**2) - self.size
		for k in range(1,self.distance+1):
			for wall in combinations(range(lower_bound,upper_bound),k):
				neighbour = self.change_position(state,wall)
				expanded = self.evaluate(neighbour)
				yield neighbour,expanded

	def execute_algorithm(self,current_solution):
		current_score = self.evaluate(current_solution)
		total_number_individuals_loop = 0
		while True:		
			end=True
			for neighbour,score in self.generate_neighbours(current_solution):
				total_number_individuals_loop+=1
				if score[0] > current_score[0]:
						current_solution = neighbour
						current_score =  score
						end=False
			#printMaze(getProblemInstance(size,current_solution))
			print("Best neighbour: {}".format(current_score[0]))
			if end:
				return current_solution,current_score,total_number_individuals_loop
			
	def RLS(self):
		sol =(0,[0],0)
		total_number_individuals = 0
		for iteration in range(self.iterations):
			print("\nIteration : {}".format(iteration))
			initial= frozenset() if iteration == 0 and self.empty else self.generate_sample()
			result=self.execute_algorithm(initial)
			sol= max(result,sol,key=lambda x: x[1][0])
			total_number_individuals+=result[2]
		print("\nREPEATED INDIVIDUALS:",total_number_individuals-self.not_repeated)
		return sol,total_number_individuals

	def ILS(self):
		maximum_number_changes = self.size**2-2*self.size
		initial = self.generate_sample()
		sol =(initial,self.evaluate(initial))
		total_number_individuals = 0
		for iteration in range(self.iterations):
			print("\nIteration : {}".format(iteration))
			if iteration == 0 and self.empty:
				initial= frozenset()   
			else:
				initial = self.change_position(initial,random.sample(range(self.size,self.size**2-self.size),min(self.num_perturbations,maximum_number_changes)))
			result=self.execute_algorithm(initial)
			sol= max(sol,result,key=lambda x: x[1][0])
			total_number_individuals+=result[2]
		print("REPEATED INDIVIDUALS:",total_number_individuals-self.not_repeated)
		return sol,total_number_individuals

	def __init__(self,size,seed,iterations,distance,num_perturbations,empty):
		self.size=size
		self.seed=seed
		self.iterations=iterations
		self.distance=distance
		self.num_perturbations=num_perturbations
		self.empty= empty
		self.not_repeated=0
		random.seed(self.seed)