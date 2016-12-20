import threading
import socket
import sys
import os.path

neighbors = []
graph = {}
mutex = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendLSA():
	# Your code goes here
	routerId = sys.argv[1]
	parentString = sys.argv[1]

	for router in neighbors:
		receiverString = '\n' + " ".join(router)

		parentString += receiverString


	for router in neighbors:
		prtNo = graph[routerId][2]

		s.sendto(parentString, ('', prtNo))

def receiveLSA():

	msg, addr = s.recvfrom(1024)

	sendingRouter = msg.readline()

	# Update graph

	if sendingRouter not in graph.keys():
		graph[sendingRouter] = []
		for line in msg:
			router, cost, prtNo = line.split()
			graph[sendingRouter].append((router, float(cost), int(prtNo)))


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
			neighbors.append((router, cost, prtNo))

	print neighbors

	s.bind(('', int(portNo)));
	
	print "Socket bound to port " + portNo

	# Initialise graph

	graph[routerId] = []

	for x in neighbors:
		graph[routerId].append((x[0], float(x[1]), int(x[2])))

	print graph

	# Initialise threads

	sendLSAThread = threading.Thread(target=sendLSA)
	receiveLSAThread = threading.Thread(target=receiveLSA)
	dijkstrasAlgoThread = threading.Thread(target=dijkstrasAlgo)

	# Start threads

	sendLSA()
	#sendLSAThread.start()
	#receiveLSAThread.start()
	#dijkstrasAlgoThread.start()

	#sendLSAThread.join()
	#receiveLSAThread.join()
	#dijkstrasAlgoThread.join()

if __name__ == '__main__':
	Main()