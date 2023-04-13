import threading
import time
import random
import select
import socket
import sys


def client(domain_lines, returned_lines):
    # Client to ts1 and ts2.py
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: LS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server

    port = int(sys.argv[1])

    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)

    ssockid1, addr = ss.accept()
    # ssockid1.send("TESTING: ".encode('utf-8'))

    queried_lines = ""
    while True:
        data_from_server = ssockid1.recv(200).decode('utf-8')
        # print("RECEIVED: ", data_from_server)
        if data_from_server != "":
            queried_lines += data_from_server
        if data_from_server == " ":
            break
        if not data_from_server:
            break
    
    # print("QUERIED: " + queried_lines)
    for line in queried_lines.split('\n'):
        domain_lines.append(line)

    domain_lines.pop()
    # print(domain_lines)
    
    hostname1_temp = sys.argv[2] + ".cs.rutgers.edu"
    port1 = int(sys.argv[3])
    hostname2_temp = sys.argv[4] + ".cs.rutgers.edu"
    port2 = int(sys.argv[5])
    # print("1: " + hostname1_temp + " : " + socket.gethostname() + " : " + str(port1) + " " + hostname2_temp + " : " + str(port2))
    localhost_addr = socket.gethostbyname(socket.gethostname())
    # connect to the server on local machine
    

    localhost_addr1 = socket.gethostbyname(hostname1_temp)
    localhost_addr2 = socket.gethostbyname(hostname2_temp)
    # print(localhost_addr)
    # print(localhost_addr1)
    # print(localhost_addr2)
    server_binding1 = (localhost_addr1, port1)
    cs1.connect(server_binding1)
    # print("Connected to TS1")

    server_binding2 = (localhost_addr2, port2)
    cs2.connect(server_binding2)
    cs1.setblocking(0)
    cs2.setblocking(0)

    # print("Connected to TS2")
    # print(domain_lines)
    received_lines = []

    for line in domain_lines:
        # print("Sending: " + line)
        cs1.send(line.encode('utf-8'))
        cs2.send(line.encode('utf-8'))
        time.sleep(1)
        ready1 = select.select([cs1],[],[],5)
        ready2 = select.select([cs2],[],[],5)

        if ready1[0]:
            data = cs1.recv(200).decode('utf-8')
            # print("GOT FROM TS1: " + data)
            received_lines.append(data) 

        elif ready2[0]:
            data = cs2.recv(200).decode('utf-8')
            # print("GOT FROM TS2: " + data)
            received_lines.append(data)
        else:
            message_to_send = line + " - TIMED OUT"
            # print(message_to_send)
            received_lines.append(message_to_send)

    # print(received_lines)
    for line in received_lines:
        # print("Sending: " + line)
        message_to_send = line + '\n'
        ssockid1.send(message_to_send.encode('utf-8'))

    ss.close()
    cs1.close()
    cs2.close()


if __name__ == "__main__":
    domain_lines = []
    # server(domain_lines)
    # print("HAVE DOMAIN LINES CHANGED?????")
    # print(domain_lines)
    # time.sleep(2)
    returned_lines = []

    client(domain_lines, returned_lines)

    # time.sleep(2)
    # print("Done. ls")