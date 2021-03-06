#!/usr/bin/env python
###########################################################
# Distributed System Assignment 2
# Multithreaded Server and Client
# File Name: tcpserver.py
# Function: Acts as a multithreaded TCP server
# Usage: In terminal "python tcpserver.py" CTRL+C to quit 
# Author: Rohail Altaf
###########################################################

# Import necessary libraries
import socket, threading, API
import functionLibrary as fL
from API import API



# threadLock is the global thread lock variable
threadLock = threading.Lock()
API = API()


# The Server object creates a TCP server and listens
# for connections made to it. Once a connection is
# made, it is passed on to the processConnection
# object 
class Server():
        TCP_ADDRESS = ''
        TCP_PORT = 6666
        global threadLock
	def __init__(self):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.TCP_ADDRESS, self.TCP_PORT))
		print "Server Initialzed\n"
        def listen(self):
                while True:
                        try:
                                self.s.listen(1)
                                self.conn, self.addr = self.s.accept()
                                self.process = processConnection(self.conn, threadLock)
                                self.process.start()
                        except KeyboardInterrupt as e:
                                print "\nGoodbye"
                                exit()

# The processConnection object spawns off a thread to
# process the connection when a client connects to the
# server
class processConnection(threading.Thread):

	# This makes every thread a daemon thread
	daemon = True
	global API
	# The initializer defines the thread lock and the
	# connection details variable
	def __init__(self, connection, lock):
		threading.Thread.__init__(self)
		self.connection = connection
		self.lock = lock

	# The run function first calls the global variable i
	# acquires the thread lock, receives the data from 
	# the client and returns the same message back along
	# with a connection ID (counter value). It then 
	# increases the counter by one, closes the connection 
	# and releases the thread lock.
	def run(self):
		self.lock.acquire()
		self.data = fL.recv(self.connection)
		dataSplit = self.data.split('|')
		print self.data
		msg = dataSplit[0]
		if(msg == "CREATE"):
			create = API.create(dataSplit[1])
			if(create == 1):
				self.connection.send("CREATE|1")
		elif(msg == "APPEND"):
			print "append"
			append = API.append(dataSplit[1], dataSplit[2], True)
			if(append):
				self.connection.send("1")
				print "1 sent for append"
		elif(msg == "READ"):
			read = API.read(dataSplit[1], 0, -1, "/var/www/fileshare/download/"+dataSplit[1])
			if(read):
				self.connection.send("1")
		elif(msg == "STREAM"):
			stream = API.stream(dataSplit[1], 0, -1, "/var/www/fileshare/download/"+dataSplit[1])
			if(stream):
				self.connection.send("1")

		elif(msg == "FILELIST"):
			filelist = API.fileList()
			filelist = filelist[1:-1]
			split = filelist.split(', ')
			string = ""
			for i in split:
				string += str(i[1:-1]) + "|"
			if(filelist):
				self.connection.send(string)
		#elif(msg == "DELETE"):

		self.connection.close()
		self.lock.release()

# This initializes the server object and then starts it
server = Server()
server.listen()
