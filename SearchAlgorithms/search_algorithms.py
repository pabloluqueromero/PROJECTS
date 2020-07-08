from collections import deque
from search_space_methods import *
from itertools import count
from heapq import heappop, heappush
from base_search_algorithm import BaseSearchAlgorithm

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
