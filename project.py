import threading
import socket
import sys
import os.path

neighbors = []
graph = {}
mutex = threading.Lock()

def sendLSA(name):


def receiveLSA(name):


def dijkstrasAlgo(name):


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

	with open(configFile, 'r') as f:
		noOfNeighbors = f.readline()[0]

		for line in f:
			neighbors.append(tuple(line.split()))

	print neighbors

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', int(portNo)));
	
	print "Socket bound to port " + portNo

	# Initialise graph

	graph[routerId] = []

	for x in neighbors:
		graph[routerId].append((x[0], float(x[1])))

	print graph

	# Initialise threads

	sendLSAThread = threading.Thread(target=sendLSA, args=("sendLSA"))
	receiveLSAThread = threading.Thread(target=receiveLSA, args=("receiveLSA"))
	dijkstrasAlgoThread = threading.Thread(target=dijkstrasAlgo, args=("dijkstrasAlgo"))

	# Start threads

	sendLSAThread.start()
	receiveLSAThread.start()
	dijkstrasAlgoThread.start()

	sendLSAThread.join()
	receiveLSAThread.join()
	dijkstrasAlgoThread.join()

if __name__ == '__main__':
	Main()