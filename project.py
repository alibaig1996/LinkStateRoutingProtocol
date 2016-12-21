import threading
import socket
import sys
import os.path
import time
import json

neighbors = []
graph = {}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendLSA():
	while True:
		time.sleep(5)
		routerId = sys.argv[1]
		parentString = sys.argv[1]

		for router in neighbors:
			receiverString = '\n' + " ".join(router)

			parentString += receiverString

		for i in neighbors:
			prtNo = graph[routerId][i[0]][1]
			s.sendto(parentString, ('localhost', prtNo))

def receiveLSA():
	while True:
		msg, addr = s.recvfrom(1024)
		msgList = msg.splitlines()

		sendingRouter = msgList[0]

		# Update graph

		if sendingRouter not in graph.keys():
			graph[sendingRouter] = {}
			for i in range(1, len(msgList)):
				router, cost, prtNo = msgList[i].split()
				graph[sendingRouter][router] =  (float(cost), int(prtNo))


		# Broadcast LSU packet to neighbours

		lst = neighbors

		for x in lst:
			if sendingRouter == x[0]:
				continue
			else:
				s.sendto(msg, ('localhost', int(x[2])))

		print json.dumps(graph, sort_keys=True, indent=4, separators=(',', ': '))


def dijkstrasAlgo():
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

	s.bind(('localhost', int(portNo)));

	# Initialise graph

	graph[routerId] = {}

	for x in neighbors:
		graph[routerId][x[0]] =  (float(x[1]), int(x[2]))

	print graph

	# Initialise threads

	sendLSAThread = threading.Thread(target=sendLSA)
	receiveLSAThread = threading.Thread(target=receiveLSA)
	dijkstrasAlgoThread = threading.Thread(target=dijkstrasAlgo)

	# Start threads

	sendLSAThread.start()
	receiveLSAThread.start()
	#dijkstrasAlgoThread.start()

	#sendLSAThread.join()
	#receiveLSAThread.join()
	#dijkstrasAlgoThread.join()

if __name__ == '__main__':
	Main()