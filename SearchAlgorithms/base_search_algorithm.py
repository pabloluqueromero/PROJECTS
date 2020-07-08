
from search_space_methods import *
class BaseSearchAlgorithm:
    def __init__(self, maze, open_nodes_data_structure, limit=float('inf'), algorithm_heuristic=None):
        self.maze = maze
        self.max_number_nodes = 0
        self.open_nodes = open_nodes_data_structure
        self.explored_states = set()
        self.limit = limit
        self.nodes_generated = 0
        self.expanded_nodes = 0
        self.size = len(maze)
        print(algorithm_heuristic)
        if algorithm_heuristic != None:
            if 1 <= algorithm_heuristic <= 3:
                self.algorithm_heuristic = [
                    self.manhattan_distance, self.manhattan_distance_improved, self.cars_already_placed][algorithm_heuristic-1]
                self.get_walls_beneath_position()
            else:
                raise Exception("Heuristic identifier must be between 1 and 3\n\t1.Manhattan Distance\n\t2.Manhattan Distance Improved\n\t1.Cars already in final position")

    def append_node(self, node):
        raise NotImplementedError("Please Implement append_node method")

    def pop_node(self):
        raise NotImplementedError("Please Implement pop_node method")

    def open_nodes_is_empty(self):
        raise NotImplementedError(
            "Please Implement open_nodes_is_empty method")

    def state_is_visited(self, node):
        raise NotImplementedError("Please Implement state_is_visited method")

    def add_visited_state(self, node):
        raise NotImplementedError("Please Implement add_visited_state method")

    # This next siz methods are used for the improved version, they will be overriden
    def get_node_cost(self, node):
        return node.path_cost

    def get_node_state(self, node):
        return node.state

    def get_node_depth(self, node):
        return node.depth

    def create_initial_node(self):
        return create_node(self.maze)

    def test_goal_state(self, node):
        return test_goal(node, self.size)

    def expand_node(self, node):
        return expand_node(self.maze, node)
    
    def recover_path(self,node):
        return recover_path(node)


    def perform_search(self):
        self.nodes_generated = 1
        self.append_node(self.create_initial_node())
        while not self.open_nodes_is_empty():
            self.max_number_nodes = max(
                len(self.open_nodes), self.max_number_nodes)
            node = self.pop_node()
            if not self.state_is_visited(node):
                if self.test_goal_state(node):
                    return self.nodes_generated, self.max_number_nodes, self.get_node_state(node), self.expanded_nodes, self.recover_path(node), self.get_node_cost(node)
                if self.get_node_depth(node) < self.limit:
                    self.expanded_nodes += 1
                    for successor in self.expand_node(node):
                        self.nodes_generated += 1
                        self.append_node(successor)
                    self.add_visited_state(node)
        return self.nodes_generated, self.max_number_nodes, None, self.expanded_nodes

    def manhattan_distance(self, state):
        total = 0
        for car in state:
            total += (self.size-1)-(car//self.size)
        return total
    #	The first heuristic returns the sum of the distances of each car to the last row we add one if there is a row in the way of a car.

    def manhattan_distance_improved(self, state):
        total = 0
        for car in state:
            total += (self.size-1) - (car//self.size)
            if car in self.number_walls:
                total += 1
        return total

    # Simple and really bad heuristic that returns the number of cars that are already in the last row.
    def cars_already_placed(self, state):
        total = 0
        for car in state:
            if(car//self.size == (self.size-1)):
                total += 1
        return total

    def get_walls_beneath_position(self):
        self.number_walls = set()
        for i in range(self.size):
            for j in range(self.size):
                for k in range(i, self.size):
                    if(self.maze[k][j] == -1):
                        self.number_walls.add(i*self.size+j)
                        break

