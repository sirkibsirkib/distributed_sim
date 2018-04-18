import random
import sys
	
#################################### INTERNALS
if len(sys.argv) != 3:
	print(("usage: python3 ./main.py <alg> <seed>\n"
		   "where: \n"
		   "       <alg> is the module name you'd like to import, in the same dir as `main`\n"
		   "       <seed> is the random seed you want for the sim\n"))
	sys.exit(0)
else:
	print(":: importing module `{}` as the algorithm".format(sys.argv[1]))
	exec("import {} as alg".format(sys.argv[1]))
	seed_num = int(sys.argv[2])
	print(":: using seed {}".format(seed_num))
	print()

	
def outgoing():
	global sender, edges_out
	return set(edges_out[sender])
	
	
def incoming():
	global sender, edges_in
	return set(edges_in[sender])
	
	
def neighbours():
	return outgoing() | incoming()
	

def send(dest, data):
	global flying_messages, sender
	print('SEND {}-->  {} data: <{}>'.format(sender, dest, data))
	flying_messages.append((1, dest, sender, data))

tasks = [
	0, #init (0, name)
	1, #send (1, dest, src, data)
]

def assertions():
	assert(type(alg.NODES) is set)
	assert(type(alg.EDGES) is set)
	for a, b in alg.EDGES:
		assert(a in alg.NODES)
		assert(b in alg.NODES)
		
		
alg.incoming = incoming		
alg.outgoing = outgoing		
alg.neighbours = neighbours
alg.send = send
	
def go():
	global sender
	global edges_out, edges_in
	global flying_messages	
	
	flying_messages = []
	assertions()
	if alg.BIDIR:
		alg.EDGES = alg.EDGES | {e[1] + e[0] for e in alg.EDGES}
	edges_out = {node: {edge[1] for edge in alg.EDGES if edge[0] == node} for node in alg.NODES}
	edges_in = {node: {edge[0] for edge in alg.EDGES if edge[1] == node} for node in alg.NODES}
	
	def get_msg():
		i = random.randint(0, len(flying_messages)-1)
		if alg.FIFO:
			# if there is an earlier message on the same channel, send that instead
			m = flying_messages[i]
			m_tup = (m[2], m[1])
			for j in range(0, i+1):
				m2 = flying_messages[j]
				if m_tup == (m2[2], m2[1]):
					return flying_messages.pop(j)
		return flying_messages.pop(i)
		
	states = {k: dict() for k in alg.NODES}
	random.seed(seed_num)
	
	for n in alg.NODES:
		sender = n
		alg.SETUP(n, states[n])
	for n in alg.INITIATORS:
		sender = n
		alg.INITIATE(n, states[n])
	
	while len(flying_messages) > 0:
		msg = get_msg()
		if msg[0] == 0:
			# init
			sender = msg[1]
			initiate(msg[1], states[msg[1]])
		if msg[0] == 1:
			# send
			sender = msg[1]
			
			print('RECV {}  -->{} data: <{}>'.format(msg[2], msg[1], msg[3]))
			alg.RECV(msg[1], states[msg[1]], msg[2], msg[3])
			

go()
			
	
		