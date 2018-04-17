import string
import random

# making A -> 'A' and AB -> ('A', 'B') for convenience
for letter in string.ascii_uppercase:
	exec("{x} = '{x}'".format(x=letter))
	for letter2 in string.ascii_uppercase:
		exec("{x}{y} = ('{x}', '{y}')".format(x=letter, y=letter2))
		
### CONFIG ################################
BIDIR = False 
FIFO = True

### NETWORK ################################

NODES = {A,B,C,D}
EDGES = {
	AB, BC, CD, DA
}

### ALGORITHM #############################

INITIATORS = {A}

# called once per node before algorithm start
def SETUP(my_name, my_state):
	global neighbours
	print('SETUP', my_name, my_state)
	pass
	
def INITIATE(my_name, my_state):
	print('{} initiating!'.format(my_name))
	for o in outgoing():
		send(o, 0)
	pass

# represents a message arriving at a destination
def RECV(my_name, my_state, sender_name, msg_data):
	if my_name not in INITIATORS:
		for o in outgoing():
			if o is not sender_name:
				send(o, msg_data+1)
	else:
		print("YAY")
	pass

"""
The following functions are available for your use
=======================================================
def outgoing():
	returns a set of names for neighbours this node can send to
	
def incoming():
	returns a set of names for neighbours this node can recv from

def neighbours():
	returns the union of outgoing() and incoming()
	
def send(dest, data):
	sends `data` to the node given the name in `dest`
=======================================================
Some useful patterns:
`if my_name in INITIATORS:`
`if 'token' in my_state and my_state['token'] == 'foo':` `
"""


