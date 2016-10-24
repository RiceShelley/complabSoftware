# relayServerModule.py <- connects to a server then connects to  a 2nd server and relays msgs between the two

import socket
import _thread as thread
import sys

# cmd line args format (server1_addr server1_port server2_addr server2_port)

# server 1 addr
server1_ip = str(sys.argv[1])
server1_port = int(sys.argv[2])

# server 2 addr 
server2_ip = str(sys.argv[3])
server2_port = int(sys.argv[4])

print(server1_ip + " " + str(server1_port) + " " + server2_ip + " " + str(server2_port))

serv1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv1.connect((server1_ip, server1_port))

serv2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv2.connect((server2_ip, server2_port))

def listen_to_server(serv1, serv2):
    while (True):
        msg = serv1.recv(1000 * 100)
        if msg == b'':
            exit()
        serv2.send(msg)

thread.start_new_thread(listen_to_server, (serv1, serv2, ))
listen_to_server(serv2, serv1)
