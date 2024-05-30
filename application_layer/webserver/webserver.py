# RRotundu 2024
# Basic webserver that returns html files

import time

import socket
import threading

#Server global variables
VERSION = 'HTTP/1.1'

# Helper to append_header
def build_header(code, string, data=""):
    s = VERSION + ' ' + str(code) + ' ' + string + "\n\n" + data
    return s

# Build reply
def append_header(code, data=""):
    match code:
        case 200:
            s = build_header(200, "OK", data)
            return s
        case 400:
            s = build_header(400, "Bad Request")
            return s
        case 404:
            s = build_header(404, "Not Found")
            return s

def handle_connection(client_socket, client_addr):
    req_msg = client_socket.recv(1024).decode()
    req_type = req_msg.split()[0]

    # Handling the different request types
    match req_type:
        case "GET":
            print("GET request received")
            req_file = req_msg.split()[1]
            try:
                f = open(req_file[1:])
            except FileNotFoundError as e:
                print(f"File {req_file} not found!")
                d = append_header(404)
                client_socket.send(d.encode())
                client_socket.close()
                return 2
            file_data = f.read()
            # append header
            print(f"Sending {req_file} to {client_addr}")
            d = append_header(200, file_data)
            client_socket.send(d.encode())
        case "POST":
            print("POST request")
        case "PUT":
            print("PUT request")
        case "DELETE":
            print("DELETE request")

    client_socket.close()
    return 0



def start_server(server_addr = '127.0.0.1', server_port = 5500):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.err as er1:
        print(f"Socket creation failed. Error: {er1}")
        return 1
    
    server_socket.bind(('',server_port))
    server_socket.listen(5)

    # Start making connections
    while 1:
        print("Waiting for connections...")
        connection_socket, client_addr = server_socket.accept()
        print(f"Connection made to client at {client_addr}")
        t = threading.Thread(target=handle_connection, args=(connection_socket, client_addr, ))
        t.start()

        # Auto shutdown
        time.sleep(30)
        return 0


if __name__ == '__main__':
    start_server()
    # return 0


