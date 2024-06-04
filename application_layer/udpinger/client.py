# RRotundu udping client exercise

import time
import socket
import sys

HOST = "127.0.0.1"
PORT = 12000
def UDP_send(msg, add_tuple, client_sock):
    client_sock.sendto(msg.encode(), add_tuple)

def ping_server(target_addr, target_port, client_sock, reps):
    for i in range(reps):
        UDP_send("echo", (target_addr, target_port), client_sock)
        ts = time.time()
        try:
            x, y = client_sock.recvfrom(1024)
            tf = time.time()
            t = tf - ts
            print(f"Ping {i} {round(t, 6)}")
        except TimeoutError as e:
            print("Timed out!")


def client_start(target_addr, target_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)
    print("Socket created with timeout 1 second")
    print(f"Starting ping to {target_addr}:{target_port}")
    ping_server(target_addr, target_port, client_socket, 10)


if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        s = sys.argv[1].split(':')
        if len(s) != 2:
            print("Usage: client.py adress:port")
        else:
            host = s[0]
            port = int(s[1])
            print(f"Starting client with target {host}:{port}")
    else:
        print(f"Starting client with default target({HOST}:{PORT})...")
        client_start(HOST, PORT)
