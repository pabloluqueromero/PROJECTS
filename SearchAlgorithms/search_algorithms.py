from collections import deque
from search_space_methods import *
from itertools import count
from heapq import heappop, heappush


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


class DepthFirstSearch(BaseSearchAlgorithm):
    def __init__(self, maze):
        super().__init__(maze, deque())

    def append_node(self, node):
        self.open_nodes.append(node)

    def pop_node(self):
        return self.open_nodes.pop()

    def open_nodes_is_empty(self):
        return len(self.open_nodes) == 0

    def state_is_visited(self, node):
        return self.get_node_state(node) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(self.get_node_state(node))


class BreadthFirstSearch(BaseSearchAlgorithm):
    def __init__(self, maze):
        super().__init__(maze, deque())

    def append_node(self, node):
        self.open_nodes.append(node)

    def pop_node(self):
        return self.open_nodes.popleft()

    def open_nodes_is_empty(self):
        return len(self.open_nodes) == 0

    def state_is_visited(self, node):
        return self.get_node_state(node) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(self.get_node_state(node))


class DepthLimitedSearch(BaseSearchAlgorithm):
    def __init__(self, maze, limit):
        super().__init__(maze, deque(), limit)

    def append_node(self, node):
        self.open_nodes.append(node)

    def pop_node(self):
        return self.open_nodes.pop()

    def open_nodes_is_empty(self):
        return len(self.open_nodes) == 0

    def state_is_visited(self, node):
        return (self.get_node_state(node), self.get_node_cost(node)) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add((self.get_node_state(node), node.path_cost))


class IterativeDeepeningSearch():

    def __init__(self, maze):
        self.maze = maze

    def depth_limited_search_instance(self, depth):
        return DepthLimitedSearch(self.maze, depth)

    def perform_search(self):
        depth = 0
        nodes_generated_total = 0
        max_number_nodes_total = 0
        expanded_nodes_total = 0
        while True:
            result = self.depth_limited_search_instance.perform_search()
            nodes_generated_total += result[0]
            max_number_nodes_total = max(result[1], max_number_nodes_total)
            expanded_nodes_total += result[3]
            if result[2] is not None:
                return nodes_generated_total, max_number_nodes_total, result[2], expanded_nodes_total, result[4], result[5]
            depth += 1


class BestFirst(BaseSearchAlgorithm):

    def __init__(self, maze, heuristic=1):
        super().__init__(maze, [], algorithm_heuristic=heuristic if heuristic!=None else 1)
        self.unique = count()

    def append_node(self, node):
        heappush(self.open_nodes, (self.algorithm_heuristic(
            self.get_node_state(node)), next(self.unique), node))

    def pop_node(self):
        return heappop(self.open_nodes)[2]

    def open_nodes_is_empty(self):
        return len(self.open_nodes) == 0

    def state_is_visited(self, node):
        return self.get_node_state(node) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(self.get_node_state(node))


class AStar(BaseSearchAlgorithm):
    def __init__(self, maze, heuristic):
        super().__init__(maze, [], algorithm_heuristic=heuristic if heuristic!=None else 1)
        self.unique = count()

    def append_node(self, node):
        heappush(self.open_nodes, (self.get_node_cost(node) +
                                   self.algorithm_heuristic(self.get_node_state(node)), next(self.unique), node))

    def pop_node(self):
        return heappop(self.open_nodes)[2]

    def open_nodes_is_empty(self):
        return len(self.open_nodes) == 0

    def state_is_visited(self, node):
        return self.get_node_state(node) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(self.get_node_state(node))


class ImprovedMixin(object):
    def create_initial_node(self):
        return create_node2(self.maze)

    def test_goal_state(self, node):
        return test_goal2(node, self.size)

    def expand_node(self, node):
        return expand_node2(self.maze, node)

    def get_node_cost(self, node):
        return node[2]

    def get_node_state(self, node):
        return node[0]

    def get_node_depth(self, node):
        return node[4]

    def recover_path(self,node):
        return recover_path2(node)


class DepthFirstSearchImproved(ImprovedMixin,DepthFirstSearch):
    def state_is_visited(self, node):
        return tuple(sorted(self.get_node_state(node))) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(tuple(sorted(self.get_node_state(node))))


class BreadthFirstSearchImproved(ImprovedMixin,BreadthFirstSearch):

    def state_is_visited(self, node):
        return tuple(sorted(self.get_node_state(node))) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(tuple(sorted(self.get_node_state(node))))


class DepthLimitedSearchImproved(ImprovedMixin,DepthLimitedSearch):
    def state_is_visited(self, node):
        return (tuple(sorted(self.get_node_state(node))), self.get_node_depth(node)) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(
            (tuple(sorted(self.get_node_state(node))), self.get_node_depth(node)))


class IterativeDeepeningSearchImproved(IterativeDeepeningSearch):
    def depth_limited_search_instance(self, depth):
        return DepthLimitedSearchImproved(self.maze, depth)


class BestFirstImproved(ImprovedMixin,BestFirst):
    def state_is_visited(self, node):
        return tuple(sorted(self.get_node_state(node))) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(tuple(sorted(self.get_node_state(node))))


class AStarImproved(ImprovedMixin,AStar):
    def state_is_visited(self, node):
        return tuple(sorted(self.get_node_state(node))) in self.explored_states

    def add_visited_state(self, node):
        self.explored_states.add(tuple(sorted(self.get_node_state(node))))
