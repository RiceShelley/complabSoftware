#client.py import time
import socket
import _thread as thread
import connHandle
from time import sleep


addrOfRelay = ('rnjupiter.ddns.net', 8024)

def connect_to_relay():
    rSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        rSock.connect(addrOfRelay)
    except socket.error:
        sleep(5)
        print("connection failed... reconnecting to server")
        rSock = connect_to_relay()
    return rSock

# connect to remote IO server
rSock = connect_to_relay()

# socket wrapper class
class sockW:
    def __init__ (self, sock, ipAddr, rSock):
        self.sock = sock
        self.ipAddr = ipAddr
        self.rSock = rSock

    def get_ip_addr(self):
        return self.ipAddr

    def get_sock(self):
        return self.sock

    def get_rSock(self):
        return self.rSock


# List of addr to connect to 
addr = ['192.168.16.53',
        '192.168.16.52', 
        '192.168.16.51',
        '192.168.16.48',
        '192.168.16.50',
        '192.168.16.54',
        '192.168.16.55',
        '192.168.16.56',
        '192.168.16.67',
        '192.168.16.66',
        '192.168.16.65',
        '192.168.16.64',
        '192.168.16.63',
        '192.168.16.62',
        '192.168.16.59',
        '192.168.16.60',
        '192.168.16.61',
        '192.168.16.58',
        '192.168.16.47',
	'192.168.16.49',
        '192.168.100.49']

#addr = ['127.0.0.1']

# List of connections
conn = []

# connect to all addr
for i in addr:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try: 
        sock.connect((i, 9800))
        rSock.send((i + " + [OK]\n").encode())
        sock_w = sockW(sock, i, rSock)
        conn_H = connHandle.connHandle(sock_w) 
        conn.append(conn_H)
    except socket.error:
        rSock.send((i + " + [BAD]\n").encode())
        continue

while (True):
    msg = rSock.recv(1000 * 100).decode()
    print(msg)
    if msg[:4] == "all ":
        for conn_H in conn:
            conn_H.step(msg[4:])
    elif msg == "ls":
        rSock.send(("\tCLIENT LIST\n<------------------------->\n").encode())
        for conn_H in conn:
            rSock.send(("| CLIENT: [" + conn_H.ip_addr + "] |\n").encode())
        rSock.send(("<------------------------->\n").encode())
    elif msg == "help":
        client = conn[0]
        client.sock.send("help".encode())
        rSock.send((client.sock.recv(1000).decode() + "\n").encode())
    elif msg[:3] == "ip ":
        msg = msg[3:]
        client_ip = msg[:msg.index(' ')]
        msg = msg[msg.index(' ') + 1:]
        for conn_H in conn:
            if conn_H.ip_addr == client_ip:
                conn_H.step(msg)
    elif msg == '':
        # somethings wrong with rSock <- reconnect
        rSock = connect_to_relay() 
    else:
        rSock.send(("UNKOWN CMD!!!\n").encode())
