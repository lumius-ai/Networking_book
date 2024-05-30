# RRotundu udping client exercise

import time
import socket

HOST = "127.0.0.1"
PORT = 12000
def UDP_send(msg, add_tuple, client_sock):
    client_sock.sendto(msg.encode(), add_tuple)

def ping_server(target_addr, target_port, client_sock, reps):
    for i in range(reps):
        UDP_send("echo", (target_addr, target_port), client_sock)
        ts = time.time()
        x, y = client_sock.recvfrom(1024)
        tf = time.time()
        t = tf - ts
        print(f"Ping {i} {t}")

def client_start(target_addr, target_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ping_server(target_addr, target_port, client_socket, 10)


if __name__ == "__main__":
    client_start(HOST, PORT)