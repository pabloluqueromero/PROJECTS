# Projects
This is a project with some samples of the different algorithms that I have studied, implemented and improved throughtour my computer engineering degree.
I will briefly explain each one.

## Metaheuristics
This project is based on the problem of the cars getting to the last row of a maze filled with walls.In this case there are 2 cars placed in both upper corners. The goal is to make the walls configuration as hard 
as possible so that the search algorithm (A*) has to expand a maximum number of nodes in order to find the optimal solution. I have implemented two different algorithms based on metaheuristics, in both of them an individual will be a configuration of walls in the maze.
- __Genetic Algorithm__
  - Simple genetic algorithm, using memoizing capabilities to avoid innecessary evaluation, with the following configurable options available:
    - Crossover probability: probability of crossing two individuals for the next generation
    - Mutation probability: probability of flipping one wall for an individual in the next generation.
    - Selection scheme: normal selection, rank selection.
    - Population combination: elitism, truncation.
    
- __Hill Climbing Algorithm__
  - Algorithm based on neighbour evaluation. For an individual of size _n_ and a distance _d_, one neighbour will be another configuration of size _n_ where exactly _d_ walls differ. We have as well some configurable parameters:
    - Distance: number of walls to be flipped in the neighbours generation (the number of neighbours grows significantly with this parameter as we are dealing with _combinations_).
    - Random Local Search or Iterative Local Search: we start the search at different points. RLS restarts the search randomly wherease ILS restarts at the last best individual (with some modifications). This is done in order to avoid local maximum.
    - Number of perturbations: number of walls that will be modified in ILS.
    - Number of iterations: number of iterations for ILS and RLS
    - Empty initial individual: starts the search from the easiest maze (no walls)
    
In order to execute the algorithms download the folder, here is an example of execution:

      
     python3 main.py 8 219 -- Genetic 200 10 1 truncation 0.95 0.1 rank
     python3 main.py 10 219 -- HillClimbing 1 1 empty ILS
