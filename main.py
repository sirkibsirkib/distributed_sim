import random

### CONFIG ################################
BIDIR = True 

### LAYOUT ################################
NODES = {'a', 'b', 'c', 'd'}
EDGES = {
	'ab',
	'bc'
}

### ALGORITHM #############################

"""
The following functions are exposed for your use

def neighbours():
	returns a set of the names for neighbours of the `current` node
	
def send(dest, data):
	sends `data` to the node given the name in `dest`
"""	

# called once per node before algorithm start
def setup(my_name, my_state):
	global neighbours
	
	print('INITIATE', my_name, my_state)
	print(neighbours())
	for n in neighbours() | {my_name}:
		send(n, (n,2,3))
	pass

# represents a message arriving at a destination
def recv(my_name, my_state, sender_name, msg_tuple):
	print('RECV {}-->{} data:[{}]'.format(sender_name, my_name, msg_tuple))
	pass
	
	
#################################### INTERNALS

def neighbours():
	global sender
	global edges
	return set(edges[sender])

def send(dest, data):
	global todo
	global sender
	print('SEND {}-->{} data:[{}]'.format(sender, dest, data))
	todo.append((1, dest, sender, data))

tasks = [
	0, #init (0, name)
	1, #send (1, dest, src, data)
]

def assertions():
	assert(type(NODES) is set)
	assert(type(EDGES) is set)
	

edges = 0
sender = 0
todo = []


def go():
	global sender
	global edges
	global todo
	global EDGES, NODES

	assertions()
	if BIDIR:
		EDGES = EDGES | {e[1] + e[0] for e in EDGES}
	edges = {node: {edge[1] for edge in EDGES if edge[0] == node} for node in NODES}
	print("edge set", edges)
	states = {k: dict() for k in NODES}
	random.seed(540)
	for n in NODES:
		sender = n
		setup(n, states[n])
	todo = []
	
	while len(todo) > 0:
		i = random.randint(0, len(todo)-1)
		print('i', i)
		print('todo:', todo)
		work = todo.pop(i)
		if work[0] == 0:
			# init
			sender = work[1]
			initiate(work[1], states[work[1]])
		if work[0] == 1:
			# send
			sender = work[1]
			recv(work[1], states[work[1]], work[2], work[3])		
go()
			
	
		