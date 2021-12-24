# Header
Madelyn Ogorek,Zhang CSCI4211,18/10/2021

Python3,server.py,,server.py
## How to Run Program:

1. run `python3 server.py` command.
2. type `exit` to kill the server program.

## Description of Program

#### main()
This part of the program is used to create the server by making the socket, binding it to the port (port 8990), and listening on it. Threading is used to allow the server to handle multiple requests at the same time.

#### dnsQuery()
This is where each clients' requests will be handled. The server first checks to see if the client has closed their connection, and if so, the server will close its socket. If not, the query is received from the client (saved in `hostname`). Then the program checks the cache (stored in the file `DNS_mapping.txt`) line by line for a matching domain name (domain names are stored as the first element in each line). If a match is found, the second element in that line (the IP address) will be appended to `ipList`. Once all the IP addresses associated with that domain name are found and added to `ipList`, `dnsSelection()` will be called to return an IP address to give to the client. If, however, a match is not found within the cache, `gethostbyname()` will be used to search for an IP address. If one exists, it will be sent to the client and added to the local cache. Otherwise "Host not found" will be sent and saved.

#### dnsSelection()
This function is used to choose one of the IP addresses associated with a given domain. The first one that was stored in the cache is arbitrarily chosen to be the one that is returned to the client.

#### monitorQuit()
This function is used to kill the server program. If "exit" is entered, it triggers the system to kill the main process.
