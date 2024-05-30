# RRotundu 2024
# Basic webserver that returns html files

import time

import socket

#Server global variables
VERSION = 'http/1.1'

def start_server(server_addr = '127.0.0.1', server_port = 1200):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.err as er1:
        print(f"Socket creation failed. Error: {er1}")
        return 1
    
    server_socket.bind(('',server_port))
    server_socket.listen(5)


if __name__ == '__main__':
    start_server()
    return 0


