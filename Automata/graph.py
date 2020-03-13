from collections import defaultdict

class Edge:
    def __init__(self,node1,node2,tag):
        self.node1 = node1
        self.node2 = node2
        self.tag=tag

class Node:
    def __init__(self,tag):
        self.tag=tag

    def __hash__(self):
        return hash(self.tag)
class Graph:
    def __init__(self,nodes =[]):
        self.nodes=nodes
        self.node_by_tag = {n.tag:n for n in nodes}
        self.edges=[]
        self.succesors = defaultdict(lambda:set())

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def add_node(self,node):
        self.nodes.append(node)
        self.node_by_tag[node.tag]=node

    def add_edge(self,edge):
        self.edges.append(edge)
        node1=self.node_by_tag[edge.node1]
        node2=self.node_by_tag[edge.node2]
        self.succesors[node1].add(node2)
