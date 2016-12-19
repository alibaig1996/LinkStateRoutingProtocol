import threading
import socket
import sys
import os.path

#def ReceiveInformation(name):


def Main():
	
	if len(sys.argv) < 4:
		print "Not enough arguments for script to execute"
		sys.exit()

	routerId = sys.argv[1]
	portNo = sys.argv[2]
	configFile = "routers\\" + sys.argv[3]

	if not os.path.isfile(configFile):
		print "Config file does not exist"
		sys.exit()

	neighbors = []
	with open(configFile, 'r') as f:
		noOfNeighbors = f.readline()[0]

		for line in f:
			neighbors.append(tuple(line.split()))

	print neighbors

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', int(portNo)));
	
	print "Socket bound to port " + portNo

	# Initialise graph

	graph = {}
	graph[routerId] = []

	for x in neighbors:
		graph[routerId].append((x[0], float(x[1])))

	print graph

if __name__ == '__main__':
	Main()