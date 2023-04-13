import threading
import time
import random
import sys
import socket


def server(DNS_dict):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: LS socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    localhost_addr = socket.gethostbyname(socket.gethostname())


    port = int(sys.argv[1])
    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    # print("[S]: LS host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    # print("[S]: LS IP address is {}".format(localhost_ip))
    csockid1, addr = ss.accept()

    # print ("[S]: Got a connection request from a client at {}".format(addr))

    input_file = []
    while True:
        data_from_server = csockid1.recv(200).decode('utf-8')
        # print("RECEIVED: ", data_from_server)

        input_file.append(data_from_server)
        if not data_from_server:
            break

        # print("Searching: " + data_from_server)
        domain = data_from_server.strip()
        domain_test = domain.lower()

        for tup in DNS_dict:
            if (tup[0].lower() == domain_test):
                message_to_send = tup[0] + " " + tup[1] + " A IN"
                # print("Sending " + message_to_send)
                csockid1.send(message_to_send.encode('utf-8'))
                break

    ss.close()
        

if __name__ == "__main__":

    DNS_dict = []

    with open("PROJ2-DNSTS2.txt") as f:
        for line in f:
            tuple = line.split()
            DNS_dict.append((tuple[0], tuple[1]))

    # time.sleep(random.random() * 5)
    server(DNS_dict)

    # time.sleep(5)
    # print("Done. LS")