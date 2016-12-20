import threading
import socket
import sys
import os.path

neighbors = []
graph = {}
mutex = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendLSA():
	print "Hi 1"

def receiveLSA():
	print "Hi 2"

	msg, addr = s.recvfrom(1024)

	sendingRouter = msg.readline()

	# Update graph

	if sendingRouter not in graph.keys():
		graph[sendingRouter] = []
		for line in msg:
			router, cost, prtNo = line.split()
			graph[sendingRouter].append(tuple(router, float(cost), int(prtNo)))


	# Broadcast LSU packet to neighbours

	lst = neighbors

	for x in lst:
		if sendingRouter == x[0]:
			continue
		else:
			s.sendto(msg, ('', x[2]))


def dijkstrasAlgo():
	mutex.acquire()
	print "Hi 3"
	mutex.release()

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
			router, cost, prtNo = line.split()
			neighbors.append(tuple(router, float(cost), int(prtNo)))

	print neighbors

	s.bind(('', int(portNo)));
	
	print "Socket bound to port " + portNo

	# Initialise graph

	graph[routerId] = []

	for x in neighbors:
		graph[routerId].append(tuple(x[0], x[1], x[2]))

	print graph

	# Initialise threads

	sendLSAThread = threading.Thread(target=sendLSA)
	receiveLSAThread = threading.Thread(target=receiveLSA)
	dijkstrasAlgoThread = threading.Thread(target=dijkstrasAlgo)

	# Start threads

	sendLSAThread.start()
	#receiveLSAThread.start()
	#dijkstrasAlgoThread.start()

	#sendLSAThread.join()
	#receiveLSAThread.join()
	#dijkstrasAlgoThread.join()

if __name__ == '__main__':
	Main()