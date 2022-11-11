from node import Node


class UnionFind:

	# Constructor
	def __init__(self):
		self.__nodes_addressed_by_value = {} # To keep track of nodes


	# Required Union-Find functions ############################################################
	def MakeSet(self, value):
		"""
			MakeSet(value):
				Makes a new set containing one node (with value 'value').
		"""
		
		# If node already exists, return it
		if self.GetNode(value):
			return self.GetNode(value)

		# Otherwise create node
		node = Node(value)

		# Keep track of node
		self.__nodes_addressed_by_value[value] = node
		
		return node


	def Find(self, x):
		"""
			Find(Node x):
				Returns the representative node of the set containing node x, by recursively 
				getting the node's parent.

			Optimisation using path compression: 
				Once you've found the root of the tree, set each visited node's parent to the 
				root, therefore flattening the tree along that path, speeding up future 
				operations.
				This is only a constant time complexity increase, but means future Find 
				operations along the same path are O(1).
		"""

		# Node is not its own parent, therefore it's not the root node
		if x.parent  != x:  
			x.parent = self.Find(x.parent) # Flatten tree as you go (Path Compression)
		
		# If node is its own parent, then it is the root node -> return it
		return x.parent


	def Union(self, x, y):
		"""
			Union(Node x, Node y):
				Performs a union on the two sets containing nodes x and y.
				Gets the representative nodes of x's and y's respective containing sets, and 
				makes one of them the other's parent (depending on their rank).

			Optimisation using union-by-rank:
				Always add the lower ranked ('smaller') tree to the larger one, ensuring no 
				increase in tree depth. If the two trees have the same rank (worst case), the 
				depth will increase by one. Without union-by-rank, each union operation is much 
				more likely to cause an increase in tree depth.
		"""

		# If x and y are the same node, do nothing
		if x == y:
			return

		# Get the roots of both nodes' trees (= the representative elements of each of their 
		# containing sets)
		x_root = self.Find(x)
		y_root = self.Find(y)

		# If x and y are already members of the same set, do nothing
		if x_root == y_root:
			return

		# Perform set union
		# Union-by-rank optimisation: always add 'smaller' tree to 'larger' tree
		if x_root.rank > y_root.rank: 
			# Tree x has higher rank (therefore 'bigger' tree), so add y to x
			y_root.parent = x_root

		elif x_root.rank < y_root.rank: 
			# Tree y has higher rank, so add x to y
			x_root.parent = y_root

		else: 
			# Trees x and y have the same rank (same 'size')
			# Therefore add one tree to other arbitrarily and increase the resulting tree's rank 
			# by one
			x_root.parent = y_root
			y_root.rank = y_root.rank + 1


	# Other functions ##########################################################################
	def GetNode(self, value): # Get node with value 'value' (O(1))
		if value in self.__nodes_addressed_by_value:
			return self.__nodes_addressed_by_value[value]
		else:
			return False


	# Debugging functions ######################################################################
	def display_all_nodes(self):
		print("All nodes:")
		for item in self.__nodes_addressed_by_value.values():
			print(item)


	def display_all_sets(self):
		sets = {} # Initialise so nodes can't be added twice

		# Add all nodes to set dictionary 
		# 	keys: representative element of each set
		#	values: the elements of the set with that representative
		for item in self.__nodes_addressed_by_value.values():
			if self.Find(item).value not in sets.keys():
				sets[self.Find(item).value] = [] # initialise list for this key
			sets[self.Find(item).value].append(item)

		# Display each representative key's set of items 
		st = ""
		for representative in sets.keys():
			st = st +  "("
			for item in sets[representative]:
				st = st + str(item.value) + ","
			st = st[:-1] # remove final ','
			st = st + ") "

		print(st)
