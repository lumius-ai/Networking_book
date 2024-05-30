# RRotundu 2024
# Basic webserver that returns html files

import time

import socket
import threading
import os

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
        case 409:
            s = build_header(409, "Conflict")
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
            print(f"Sending {req_file[1:]} to {client_addr}")
            d = append_header(200, file_data)
            client_socket.send(d.encode())
            print("Data sent!")
        case "POST":
            print("POST request received")
            req_file = req_msg.split()[1]
            data = req_msg.split("\n\n")[-1]
            try:
                f = open(req_file[1:], "x")
                f.write(data)
                f.close()
                client_socket.send(append_header(200).encode())
            except FileExistsError as e:
                print("File already exists!")
                h = append_header(409)
                print(h)
                client_socket.send(h.encode())
                client_socket.close()
            



        case "PUT":
            print("PUT request")
        case "DELETE":
            print("DELETE request received")
            req_file = req_msg.split()[1]
            try:
                os.remove(req_file)
                h = append_header(200)
                print(h)
                client_socket.send(h.encode())
                client_socket.close()
            except FileNotFoundError as e:
                h = append_header(404)
                print(h)
                client_socket.send(h.encode())
                client_socket.close()

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


