# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

try:
    set()
except NameError:
    from sets import Set as set, ImmutableSet as frozenset

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
	visited = set()				#Must be implemented correctly! #Lets hope it is!
	agenda = list()				#is a queue

	agenda.append([start]);

	while (True):
		if (len(agenda) == 0):
			return []

		cur_path = agenda.pop(0)
		cur_node = cur_path[-1]

		if (cur_node == goal):
			return cur_path

		visited.add(cur_node)

		for branching_node in graph.get_connected_nodes(cur_node):
			#add path with connected node to the agenda (FIFO)
			#extend the next 'current node' which is determined 
			#by popping the FIFO and taking the last element of that path
			if (branching_node in visited):
				continue

			agenda.append(cur_path + [branching_node])
			

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
	visited = set()					#Must be implemented correctly! #Lets hope it is!
	agenda = list()					#Is a Stack

	agenda.append([start])

	while (True):
		if (len(agenda) == 0):
			return []

		cur_path = agenda.pop(-1)
		cur_node = cur_path[-1]

		if (cur_node == goal):
			return cur_path

		visited.add(cur_node)

		for branching_node in reversed(graph.get_connected_nodes(cur_node)):
			#add path with connected node to the agenda (LIFO)
			#extend the next 'current node' which is determined
			#by popping the LIFO and taking the last element of that path
			if(branching_node in visited):
				continue

			agenda.append(cur_path + [branching_node])


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
	""" Agenda = [path1, path2, path3, etc]
		path = [node1, node2, node3]
		queue like agenda FIFO
	"""
	#Initializing Agenda with start node
	agenda = list()
	agenda.append([start])

	while (True):
		#Getting the node to be looked at
		if (0 < len(agenda)):
			cur_path = agenda.pop(-1)
			cur_node = cur_path[-1]
			cur_heuristics = graph.get_heuristic(cur_node, goal)
		else:
			return []

		#Exit if the current node is the goal
		if (cur_node == goal):
			return cur_path
	
		cur_possible_branches = []

		for branching_node in graph.get_connected_nodes(cur_node):
			branching_heur = graph.get_heuristic(branching_node, goal)
			#Skip if regarded node is in current paths	##Should actually be taken care of in the next section
			if (branching_node in cur_path):
				continue

			cur_possible_branches.append([branching_heur, branching_node])

		cur_possible_branches = reversed(sorted(cur_possible_branches))
		agenda += [ cur_path + [ x[1] ] for x in cur_possible_branches]

		


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
	agenda = list()				#is a queue

	agenda.append([start]);

	while (True):
		if (len(agenda) == 0):
			return []

		cur_path = agenda.pop(0)
		cur_node = cur_path[-1]

		if (cur_node == goal):
			return cur_path

		all_branches = []
		for branching_node in graph.get_connected_nodes(cur_node):
			if (branching_node in cur_path):
				continue
			all_branches.append([graph.get_heuristic(branching_node, goal), branching_node])

		all_branches = sorted(all_branches)
		all_branches = all_branches[:beam_width]
		#for x in all_branches:
		#if (x in sorted_branches):
		#		agenda += [cur_path + [x[1]]]
		agenda +=  [(cur_path + [x[1]]) for x in all_branches ] 




## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
	if (len(node_names)<2):
		return 0
	tot_sum = 0
	for i in xrange(0, len(node_names)-1):
		cur_edge = graph.get_edge(node_names[i], node_names[i+1])
		tot_sum += cur_edge.length
	return tot_sum

def branch_and_bound(graph, start, goal): 
	agenda = list()

	agenda.append([0, [start]]);

	#flag = False

	while (True):
		if (len(agenda) == 0):
			return []

		agenda_item = agenda.pop(0)
		cur_path = agenda_item[1]
		cur_node = cur_path[-1]

		if (cur_node == goal):
			#if (flag):
			return cur_path
			#else:
		#		flag = True
#			flag = true
#			return cur_path

		for branching_node in graph.get_connected_nodes(cur_node):
			if (branching_node in cur_path):
				continue
			node_length = path_length(graph, cur_path + [branching_node] )
			agenda.append([node_length, cur_path + [branching_node]])
		agenda = sorted(agenda)	
		print agenda
		print
	print
	print
	
def a_star(graph, start, goal):
	visited = set()
	agenda = list()
	
	start_heuristics = graph.get_heuristic(start, goal)
	agenda.append([start_heuristics, [start]])

	while(True):
		if( len(agenda) == 0):
			return []

		agenda_item = agenda.pop(0)
		cur_path = agenda_item[1]
		cur_node = cur_path[-1]

		if(cur_node == goal):
			return cur_path

		for branching_node in graph.get_connected_nodes(cur_node):
			if (branching_node in cur_path) or (branching_node in visited):
				continue
			node_length = path_length(graph, cur_path + [branching_node] )
			node_heuristics = graph.get_heuristic(branching_node, goal)

			agenda.append([node_length + node_heuristics, cur_path + [branching_node]])
		agenda = sorted(agenda)


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
	for node in graph.nodes:
		plength = path_length(graph, bfs(graph, node, goal) )
		eheur = graph.get_heuristic(node, goal)
		if (eheur > plength):
			return False 
	return True 
		
def is_consistent(graph, goal):
	for edge in graph.edges:
		edge_length = edge.length
		h1 = graph.get_heuristic(edge.node1, goal)
		h2 = graph.get_heuristic(edge.node2, goal)
		diff_heuristic = abs(h1 - h2)
		if not (edge_length >= diff_heuristic):
			return False
	return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '10'
WHAT_I_FOUND_INTERESTING = 'Nothing but the G-Thang'
WHAT_I_FOUND_BORING = 'Nate Dogg'
