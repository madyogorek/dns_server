# Fall 2021 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os, random
from socket import *

def main():
	host = "localhost" # Hostname. It can be changed to anything you desire.
	port = 8990 # Port number.

	#create a socket object, SOCK_STREAM for TCP
	try:
		mySocket = socket(AF_INET, SOCK_STREAM)
		print("successfully created socket")
	except error as e:
		print("socket creation failed : %s" %(e))
		mySocket = None

	#bind socket to the current address on port

	try:
		mySocket.bind((host, port))
	except error as msg:
		mySocket = None # Handle exception
		#print("hey")


	#Listen on the given socket maximum number of connections queued is 20
	try:
		mySocket.listen(20)
	except error as msg:
		mySocket = None # Handle exception


	if mySocket is None:
		print("Error: cannot open socket")
		sys.exit(1) # If the socket cannot be opened, quit the program.

	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()

	print("Server is listening...")

	while 1:
		#blocked until a remote machine connects to the local port
		connectionSock, addr = mySocket.accept()
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		server.start()

def dnsQuery(connectionSock, srcAddress):

	#get data from the client
	hostName = connectionSock.recv(1024).decode()

	if not hostName:
		connectionSock.close()
		return
	#check the DNS_mapping.txt to see if the host name exists
	#create file if it doesn't exist
	try:
		myCache = open("DNS_mapping.txt", 'r')
	except error as msg:
		myCache = open("DNS_mapping.txt", 'x')
		myCache.close()
		myCache = open("DNS_mapping.txt", 'r')

	logEntry = ""
	response = ""

    #if it does exist, read the file line by line to look for a
	#match with the query sent from the client
	ipAddress = ""
    #If match, use the entry in cache.
	ipList = []
	for line in myCache:
		templst = line.strip('\n').split(",")
		if(templst[0] == hostName):
			ipList.append(templst[1])
	myCache.close()
	if(len(ipList) > 0):
		#However, we may get multiple IP addresses in cache, so call dnsSelection to select one.
		ipAddress = dnsSelection(ipList)
		response = hostName + ":" + ipAddress + ":CACHE"
		logEntry = hostName + "," + ipAddress + ",CACHE\n"
		myCache = open("DNS_mapping.txt", 'a')
		myCache.write(hostName + ',' + ipAddress + '\n')
		myCache.close()
	else:
		#not found in cache
		#If no lines match, query the local machine DNS lookup to get the IP resolution
		try:
			ipAddress = gethostbyname(hostName)
		except error:
			ipAddress = "Host not found"
        #write the response in DNS_mapping.txt
		myCache = open("DNS_mapping.txt", 'a')
		myCache.write(hostName + ',' + ipAddress + '\n')
		myCache.close()
		logEntry = hostName + "," + ipAddress + ",API\n"
		response = hostName + ":" + ipAddress + ":API"

	logFile = open("dns-server-log.csv", 'a')
	logFile.write(logEntry)
	logFile.close()
	#print response to the terminal
	print("Response: " + response)
	#send the response back to the client
	connectionSock.send(response.encode())
	#Close the server socket.
	connectionSock.close()

def dnsSelection(ipList):
	#checking the number of IP addresses in the cache
	#if there is only one IP address, return the IP address
	return ipList[0]
	#if there are multiple IP addresses, select one and return.
	##optional: return the IP address according to the Ping value for better performance (lower latency)


def monitorQuit():
	while 1:
		sentence = input()
		if sentence == "exit":
			os.kill(os.getpid(),9)

main()
