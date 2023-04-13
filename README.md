# Python socket server and receiver with load balancing

Project designed to replicate DNS servers and spreading using python sockets. 

This is done through using TS1.py and TS2.py as the two DNS servers, LS which is the laod balacing server, and client.py which is sending out the requests with domain names and receiving the IP addresses. 
PROJ2.DNSTS1.txt contains the DNS table of TS1 and PTOJ2-DNSTS2.txt contains the DNS table of TS2. 

LS the load balancing server receives a request from the client and sends it to both TS1 and TS2, if it gets a response it will send it back to the client, oterwise it will send a timed out mesasge. 
