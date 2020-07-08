# Projects
This is a project with some samples of the different algorithms that I have studied, implemented and improved throughout my computer engineering degree.
I will briefly explain each one of them.

## State space search
This section is a recopilation of path finding algorithms. In this case the goal is to take _n_ cars form the top row of a maze filled with obstacles (walls) to the bottom row. Cars are randomly placed in the first row, where there can be no walls and the walls are distributed in the remaining rows except the last one. Cars can't travel diagonally, only one car may move at a time and the cost of each movement is 1 unit.
I have used inheritance in order to allow code reutilisation and show how similar all of these algoritms are. There are slight changes in the data structures used, as well as differences regarding uninformed search vs informed search, thereof relying on priority based data structures (heaps in this case).
The algorithms implemented are:

- __Uninformed__
  - Depth First Search
  - Breadth First Search
  - Depth First Limited Search
  - Iterative Deepening Depth-First Search

- __Informed__
  - Best First
  - A*
  
There are some parameters that need to be configured such as:
  - Size of the maze
  - Number of Cars
  - Seed
  - Algorithm to be used
  - Optional parameters: heuristic (for informed algorithms), limit(for depth limited search).
There are 3 different heuristics available:
  - Manhattan Distance: well-known heuristic, where we add the distance to the last row of each.
  - Manhattan Distance Improved: same heuristic however we add +1 for each car with a wall in its way.
  - Number of cars in the last row.
 
 There is an improved version of each algorithm (time and space improvement). For _n_ cars, any _variation_ will yield the same set of actions therefore we don't need to evaluate it again if the cars are in the same positions but in different order.
 
 Here are some examples of how to execute the algorithms:
 
     python3 execute_algorithms.py size n_cars seed -- algorithm optional_args
     python3 execute_algorithms.py 10 3 209 -- AStarImproved 1
     python3 execute_algorithms.py 20 4 0 -- DepthFirstSearch

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
