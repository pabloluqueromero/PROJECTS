class Node():
	__slots__ = 'state','parent_node','path_cost','action','depth'
	def __init__(self,state,parent_node=None,path_cost=0,action=None,depth=0):
		self.state= state
		self.parent_node=parent_node
		self.path_cost=path_cost
		self.action=action
		self.depth=depth

