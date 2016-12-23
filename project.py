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
	time.sleep(10)
	while True:
		time.sleep(1)
		routerId = sys.argv[1]
		parentString = ""

		for x in neighbours:
			parentString += x[0]

		parentString += '\n' 
		parentString += routerId

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

		sendLst = list(msgList[0])
		sendingRouter = msgList[1]

		# Update graph

		if sendingRouter not in graph.keys():
			graph[sendingRouter] = {}
			for i in range(2, len(msgList)):
				router, cost, prtNo = msgList[i].split()
				graph[sendingRouter][router] =  (float(cost), int(prtNo))


		# Broadcast LSU packet to neighbours

		del msgList[0]
		lst = neighbors
		n = []

		for x in lst:
			n.append(x[0])

		neighborsToSend = [x for x in n if n not in sendLst]
		msg2 = ''.join(neighborsToSend) + ''.join(sendLst) + '\n' + '\n'.join(msgList)


		for x in neighborsToSend:
			if sendingRouter == x[0]:
				continue
			else:
				s.sendto(msg2, ('localhost', int(x[2])))

def dijkstrasAlgo():
	while True:
		time.sleep(30)
		print json.dumps(graph, sort_keys=True, indent=4, separators=(',', ': '))
		print ""
		print "I am router " + sys.argv[1]
		visited = {}
		unvisited = {}
		paths = {}
		for n in graph.keys():
			unvisited[n] = None
			paths[n] = None

		currentNode = sys.argv[1]
		currentNodeDistance = 0
		unvisited[currentNode] = currentNodeDistance

		while True:
			for n, d in graph[currentNode].items():
				if n not in unvisited: 
					continue
				newDistance = currentNodeDistance + d[0]
				if unvisited[n] is None or unvisited[n] > newDistance:
					unvisited[n] = newDistance
					paths[n] = currentNode

			visited[currentNode] = currentNodeDistance
			del unvisited[currentNode]

			if not unvisited: 
				break

			candidates = []
			for n in unvisited.items():
				if n[1]:
					candidates.append(n)

			currentNode, currentNodeDistance = sorted(candidates, key = lambda x: x[1])[0]

		nodes = graph.keys()
		nodes.remove(sys.argv[1])

		for i in nodes:
			lst = []
			target = i

			while paths[i]:
				lst.insert(0, i)
				i = paths[i]

			lst.insert(0, i)
			print "Least cost path to router " + target + ": " + ''.join(lst) + " and the cost is: " + str(visited[target])

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