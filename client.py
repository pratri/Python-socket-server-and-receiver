# host = socket.gethostname() localhost_ip = (socket.gethostbyname(host)) server_binding = (host, ts1listenPort) ss.bind(server_binding) ss.listen(1) csockid, addr = ss.accept()

import threading
import time
import random
import select
import socket
import sys



def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: LS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # Define the port on which you want to connect to the server
    # localhost_addr = socket.gethostbyname(socket.gethostname())
    hostname_temp = sys.argv[1] + ".cs.rutgers.edu"

    port = int(sys.argv[2])
    localhost_addr = socket.gethostbyname(hostname_temp)
    # print("NAME: " + hostname_temp + " : " + localhost_addr)

    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    # print("Connected to LS")

    # print(cs.recv(200).decode('utf-8'))

    with open("PROJ2-HNS.txt") as f:
        for line in f:
            # print("SENDING: ", line)
            cs.send(line.encode('utf-8'))
            time.sleep(1)

    cs.send(" ".encode('utf-8'))

    time.sleep(2)
    # Have code waiting for message from ls

    # cs.setblocking(0)
    # print("BLOCKING???")
    # select.select([cs], [], [])

    input_file = ""
    while True:
        data_from_server = cs.recv(200).decode('utf-8')
        # print("RECEIVED: ", data_from_server)

        input_file += data_from_server
        if not data_from_server:
            break
    
    final_lines = input_file.split('\n')
    f = open("RESOLVED.txt", "w")

    for line in final_lines:
        # print(line)
        f.write(line + "\n")
    f.close()

    cs.close()

if __name__ == "__main__":

    # time.sleep(random.random() * 5)
    client()

    time.sleep(2)
    print("Done. clinet")