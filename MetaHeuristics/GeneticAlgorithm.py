
import random
from utils import memoize,A_StarImproved,getWallsBeneathPositions,heuristic2,get_max_mean
class GeneticAlgorithm:
	
	@memoize(equivalent=True)
	def evaluate(self,individual):
		self.not_repeated+=1
		return A_StarImproved(individual,self.size,heuristic2,getWallsBeneathPositions(individual,self.size))

	def fitness(self,population):
		evaluation=[]
		for individual in population:
			evaluation.append([individual,evaluate(individual)])
		return evaluation

	def generate_population(self):
		population = []
		for _ in range(self.number_individuals):
			possible_walls = range(self.size,(self.size**2)- self.size)
			random_size = random.randint(0,(self.size**2)-2*self.size)
			population.append(frozenset(random.sample(possible_walls,random_size)))
		return population

	def mutate(self,population):
		new_population = []
		for individual in population:
			if random.random()<self.mutation_probability:
				individual = set(individual)
				wall = random.choice(range(self.size,self.size**2-self.size))
				if wall in individual:
					individual.remove(wall)
				else:
					individual.add(wall)
				individual = frozenset(individual)
			new_population.append(individual)
		return new_population

	def elitism (self,population1,population2):
		maximum = max(population2,key= lambda x :x[1][0])
		minimum_index = min(enumerate(population1),key= lambda x :x[1][1][0])[0]
		population1[minimum_index] = maximum
		return population1

	def truncation(self,population1,population2):
		return sorted(population1 + population2,reverse = True,key= lambda x :x[1][0])[:len(population1)]

	def crossover(self,population):
		new_population = []
		possible_crossover_points = range(self.size+1,self.size**2-self.size)
		minimum =min(self.number_points,self.size*(self.size-2)-1)
		last = self.size**2-self.size
		for individual1, individual2 in zip(population, population[1:]):
			if random.random() < self.crossover_probability:
				i1 =individual1[0]
				i2 = individual2[0]
				elements = [self.size]+sorted(random.sample(possible_crossover_points,minimum))+[last]
				offspring1= set()
				offspring2 = set()

				for point in range(len(elements) - 1):
					section =set(range(elements[point],elements[point+1]))
					offspring1 |=  section.intersection(i1)
					offspring2 |= section.intersection(i2)
					i1,i2 = i2,i1
					
				new_population.append(frozenset(offspring1))
				new_population.append(frozenset(offspring2))
				
			else:
				new_population.append(individual1[0])
				new_population.append(individual2[0])
		return new_population

	def select_population(self,population):
		selected_individuals = []
		num_selected = len(population)
		totalFitness = sum(population_value[0] for _,population_value in population)
		for _ in range(num_selected):
			cumulative_prob = 0.0
			r = random.random()
			for individual in population:
				cumulative_prob += individual[1][0]/totalFitness
				if  r <= cumulative_prob:
					selected_individuals.append(individual)
					break
		return selected_individuals

	def select_population_rank(self,population):
		selected_individuals = []
		num_selected = len(population)
		totalRank = (num_selected * (num_selected+1))/2
		population.sort(reverse = True, key= lambda x :x[1][0])
		for _ in range(num_selected):
			cumulative_prob = 0.0
			r = random.random()
			for i,individual in enumerate(population,start=1):
				cumulative_prob += (num_selected-i+1)/totalRank
				if  r <= cumulative_prob:
					selected_individuals.append(individual)
					break
		return selected_individuals

	def execute_algorithm(self):
		random.seed(self.seed)
		population = self.generate_population()
		population_with_fitness = self.fitness(population)
		for generation in range(self.generations):
			selected_individuals = self.selection(population_with_fitness)
			crossed_individuals = self.crossover(selected_individuals)
			mutated_individuals = self.mutate(crossed_individuals)
			new_population = self.fitness(mutated_individuals)
			population_with_fitness = self.combine(population_with_fitness,new_population)

			#Obtaining population's statistics
			best,mean = get_max_mean(population_with_fitness)
			print("Generation {} population length: {}\nMean fitness: {}\nBest fitness: {}\n".format(generation, len(population_with_fitness),mean,best))
		
		print("REPEATED INDIVIDUALS:",self.number_individuals*2*self.generations-self.not_repeated)
		return population_with_fitness

	def __init__(self,size,seed,individuals,generations,number_points,crossover_probability,mutation_probability,selection,combine):
		self.size = size
		self.seed = seed
		self.number_individuals = individuals
		self.generations = generations
		self.number_points = number_points
		self.crossover_probability = crossover_probability
		self.mutation_probability = mutation_probability
		self.selection = self.select_population_rank if "rank" in selection else self.select_population
		self.combine = self.elitism if "elit" in combine else self.truncation
		self.not_repeated=0
